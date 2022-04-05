<template>
  <div id="app">
    <b-container>
      <Nav />
      <router-view/>
    </b-container>
  </div>
</template>

<script>
import axios from "axios"
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import Nav from "./components/Nav";


export default {
  name: 'App',

  components: {
    Nav
  },

  created() {
    this.$store.commit('InitializeStore')
    const token = this.$store.state.token

    if (token) {
      axios.defaults.headers.common['Authorization'] = 'Token '+ token
    } else {
      axios.defaults.headers.common['Authorization'] = ''
    }
  }
}

</script>

<style>

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background-color: #39657c;
  min-height: 100vh;
  padding-bottom: 1em;
}

.card {
  background-color: #2d5a77;
  border-radius: 20px;
  margin-top: 10px;
  margin-bottom: 10px;
}

.item {
  border: solid 1px;
  border-color: #c9fa69;
  border-radius: 20px;
  background-color: #2f526c;
 
}

h2, h1, h3, h4, label {
  color: #f9f6f4;
}


.btn  {
  border-radius: 12px;
  background-color:#223951;
  color: #c9fa69;
  padding-left: 23px;
  padding-right: 23px;
  margin: 12px;
}

.btn:hover {
  background-color:#223951;
  color: #c9fa69;
}

.btn:focus {
  color:#c9fa69;
  background-color:#223951;
  box-shadow: 0px 0px 5px 2px #c9fa69;
}

p {
  color: #f9f6f4;
}
</style>
