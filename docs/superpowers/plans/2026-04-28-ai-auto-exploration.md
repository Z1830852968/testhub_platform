# AI Auto-Exploration Feature Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform the hardcoded "System Auto Exploration" into a real, dynamic AI-driven visual web spider that interacts with the target web application, configured dynamically per-run.

**Architecture:** 
1. **Frontend**: Update `AISystemExploration.vue` to allow users to configure the exploration run: `Base URL`, `Auth Type` (None/Form), `Username/Password`, and `Max Steps`.
2. **Backend Models**: Expand `AIModelConfig` roles to include `explorer`. Add configuration fields to `ExplorationRun`.
3. **Backend Engine**: Overhaul the Celery task `run_system_exploration` in `apps/explorations/tasks.py`. It will launch Playwright, perform login if configured, and enter an exploration loop. In each step, it will extract interactive elements (buttons/links) from the DOM, pass them to the configured AI Model via `AIModelService`, parse the AI's decision (what to click and what feature it discovered), execute the click, and save the result as a `FeatureItem`.

**Tech Stack:** Vue3 + Element Plus, Django REST Framework, Celery, Playwright, LLM integration (`AIModelService`).

---

### Task 1: Update Backend Models & ViewSet

**Files:**
- Modify: `apps/requirement_analysis/models.py`
- Modify: `apps/explorations/models.py`
- Modify: `apps/explorations/views.py`
- Modify: `apps/explorations/serializers.py`

- [ ] **Step 1: Add 'explorer' role to AIModelConfig**
Update `ROLE_CHOICES` in `apps/requirement_analysis/models.py` to include `('explorer', 'AI网页探索专家')`.

- [ ] **Step 2: Add Config Fields to ExplorationRun**
In `apps/explorations/models.py`, add the following to `ExplorationRun`:
```python
    base_url = models.URLField(blank=True, null=True)
    auth_type = models.CharField(max_length=20, default='none') # 'none', 'form'
    auth_username = models.CharField(max_length=100, blank=True, null=True)
    auth_password = models.CharField(max_length=100, blank=True, null=True)
    max_steps = models.IntegerField(default=10)
```

- [ ] **Step 3: Update Serializer**
In `apps/explorations/serializers.py`, update `ExplorationRunSerializer` to include the new fields.

- [ ] **Step 4: Update ViewSet**
In `apps/explorations/views.py`, ensure the `create` method extracts these fields from `request.data` and passes them to the `ExplorationRun` instance. Ensure the `run_id` is still passed to the task.

- [ ] **Step 5: Apply Migrations**
Run `python manage.py makemigrations explorations requirement_analysis` and `python manage.py migrate`.

### Task 2: Implement the AI Spider Engine in Celery

**Files:**
- Modify: `apps/explorations/tasks.py`

- [ ] **Step 1: Implement DOM extraction script**
In `tasks.py`, write a JS snippet string that injects `data-ai-id` into all `a, button, input` elements and returns a JSON list of their IDs, tag names, and inner text/values.

- [ ] **Step 2: Re-write `run_system_exploration`**
Modify the task to:
1. Retrieve `ExplorationRun` and its configurations.
2. Retrieve the `AIModelConfig` where `role='explorer'`. If none exists, fall back to any available or fail.
3. Launch Playwright and navigate to `run.base_url`.
4. If `run.auth_type == 'form'`, fill `input[type="text"], input[name="username"]` and `input[type="password"]` and click submit. Wait.
5. Loop `run.max_steps` times:
   - Check `is_stopped(run_id)`.
   - Run the DOM extraction script via `page.evaluate()`.
   - Formulate a prompt: "You are exploring a web app. Current URL: {url}. Interactive elements: {elements}. Describe the current page's feature briefly (feature_name, description) and choose the next element ID to click to explore further. Return JSON: {\"feature_name\": \"...\", \"description\": \"...\", \"next_action_id\": \"...\"}".
   - Call `async_to_sync(AIModelService.call_openai_compatible_api)(model_config, messages)`.
   - Parse the JSON response.
   - Take a screenshot and save `FeatureItem` and `ExplorationArtifact` with the AI's `feature_name` and `description`.
   - Find the element by `[data-ai-id="..."]` and click it. `page.wait_for_timeout(3000)`.

### Task 3: Update Frontend Exploration Config

**Files:**
- Modify: `frontend/src/views/ai-intelligent-mode/AISystemExploration.vue`

- [ ] **Step 1: Add Configuration Form Fields**
Add fields to `form` ref: `base_url`, `auth_type` (radio/select: 无/表单登录), `auth_username`, `auth_password`, `max_steps` (number, default 10).
Add the corresponding `<el-form-item>` UI elements in the template.

- [ ] **Step 2: Update Payload in `startExploration`**
Pass these new fields in the `api.post('/explorations/runs/')` payload.

- [ ] **Step 3: Update Table Display (Optional)**
Display `base_url` or `max_steps` in the runs table to provide better visibility into what was configured.

### Task 4: Testing & Verification

- [ ] **Step 1: Test Database Migrations**
Run the backend and ensure no errors.
- [ ] **Step 2: Test Form Submission**
Verify the frontend sends the correct configuration.
- [ ] **Step 3: Test AI Exploration Run**
Start an exploration. Check celery logs to ensure it queries the LLM and clicks elements dynamically. Verify `FeatureItem` entries are populated with AI-generated descriptions rather than hardcoded ones.
