<template>
  <div class="body">
    <form class='login-form' @submit.prevent="submitForm">
      <div class="flex-row logo mt-3">
        <h1>Вход</h1>
      </div>
      <div class="flex-row m-4">
        <input v-model="username"  class='inp' placeholder='Your username' type="text">
      </div>
      <div class="flex-row">
        <input v-model="password" id="password" class='lf--input inp' placeholder='Your password' type='password'>
      </div>
      <div ref="val" class="validate">
        <label class="valid">Неверный логин или пароль</label>
      </div>
      <b-button  class='lf--submit mt-4' type='submit' value='Sign Up'>Войти</b-button>
    </form>
  </div>

</template>

<script>
import axios from "axios";

export default {
  name: "Login",
  data() {
    return {
      username: '',
      password: ''
    }
  },

  methods: {
    async submitForm() {
      const formData = {
        username: this.username,
        password: this.password
      }
      await axios
          .post('auth/token/login', formData)
          .then(response => {
  
            const token = response.data.auth_token

            axios.defaults.headers.common['Authorization'] = ''

            this.$store.commit('setToken', token)

            axios.defaults.headers.common['Authorization'] = 'Token '+ token

            localStorage.setItem('token', token)

            this.$router.push('/survey')


          })
          .catch(error => {
            if (error.response.status===400 || error.response.status===401){
              this.$refs.val.style.display ='block'
          }})
    },

  }

}
</script>



<style scoped>

.inp {
  border-radius: 12px;
  background-color: #2d5a77;
  border-color: #223951;
  color: aliceblue;
  width: 300px;
}

.inp:focus {
  border: 1px solid #c9fa69;
  box-shadow: 0px 0px 5px 2px #c9fa69;
}

.valid {
  font-size: 16px;
  font-weight: 600;
  margin-top: 20px;
  color: #EB5BB1;
}

.validate {
  display: none
}

</style>