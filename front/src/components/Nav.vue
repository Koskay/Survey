<template>
  <div>
    <b-row>
    <b-navbar toggleable type="dark" class="py-3" style="background-color:#223951; border-radius:15px;">
      <b-navbar-brand href="#">{{this.$store.getters.getUsers.username}}</b-navbar-brand>

      <b-navbar-toggle target="navbar-toggle-collapse">
        <template #default="{ expanded }">
          <b-icon v-if="expanded" icon="chevron-bar-up"></b-icon>
          <b-icon v-else icon="chevron-bar-down"></b-icon>
        </template>
      </b-navbar-toggle>

      <b-collapse id="navbar-toggle-collapse" is-nav>
        <b-navbar-nav class="ml-auto">
          <div v-if="$store.state.isAuthenticated">
            <b-nav-item href="#" @click="goTo">Главная</b-nav-item>
            <b-nav-item href="#" @click="logout">Выйти</b-nav-item>
          </div>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
    </b-row>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "Nav",

  data(){
    return{
      username: ''
    }
  },


  methods: {

    goTo() {
      if (this.$route.name !== 'Survey') this.$router.push("/survey");
    },

    logout(){
      this.$store.state.token = ''
      localStorage.clear()
      this.$store.commit('removeToken')
      this.$store.commit('removeUsers')
      axios
          .post('auth/token/logout/')

      axios.defaults.headers.common['Authorization'] = ''

      this.$router.push(({name: 'Login'}))
    },
  },

}
</script>

<style scoped>

</style>