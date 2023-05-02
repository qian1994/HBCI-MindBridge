<template>
  <div class="homepage">
    <div class="login-container">
      <el-form :model="formData" ref="ruleForm" label-width="100px" class="demo-ruleForm">
        <el-form-item label="用户名" prop="name">
          <el-input v-model="formData.name"></el-input>
        </el-form-item>
        <el-form-item label="用户id" prop="id">
          <el-input v-model="formData.id"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="formData.password"></el-input>
        </el-form-item>
        <el-form-item >
          <el-button size="large" @click="submit"> 登录 </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      formData: {
        id: '',
        name: '',
        password: '',

      }
    }
  },
  methods:{
    submit() {
      if(this.formData.name == '') {
        this.$message('请输入用户名')
        return
      }

      if(this.formData.password == '') {
        this.$message('请输入密码')
        return
      }

      if(this.formData.id == '') {
        this.$message('请输入密码')
        return
      }

      this.$router.push({name: 'pannels', params:{...this.formData}})
    }
  }
};
</script>

<style>
.login-container {
  width: 500px;
  margin: 300px auto;
  background-color: white;
  padding: 30px ;
  box-sizing: border-box;
}
</style>
