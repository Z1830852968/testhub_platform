import re

with open('frontend/src/views/requirement-analysis/RequirementAnalysisView.vue', 'r') as f:
    content = f.read()

# Add mounted hook to read query params
script_setup_match = "export default {"

mounted_hook = """  mounted() {
    this.checkConfigStatus()
    
    // 从路由读取上下文数据 (如果从 AI 工作成果跳转过来)
    if (this.$route.query.title || this.$route.query.desc) {
      if (this.$route.query.title) {
        this.manualInput.title = this.$route.query.title
      }
      if (this.$route.query.desc) {
        this.manualInput.description = this.$route.query.desc
      }
      
      // 自动展开手动输入区域并提示
      ElMessage.success('已自动填充系统探索提取的功能点信息，您可以直接生成测试用例')
    }
  },"""

# Replace the existing mounted hook if it exists, or insert it.
if "mounted() {" in content:
    # We need to carefully replace it.
    pass

# Let's find mounted in the file.
