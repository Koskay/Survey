import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    token: '',
    isAuthenticated : false,
    backendUrl: 'http://127.0.0.1:8000/api',
    user: [],
    users: []
  },
  mutations: {
    InitializeStore(state){
      if (localStorage.getItem('token')) {
        state.token = localStorage.getItem('token')
        state.isAuthenticated = true
      } else {
        state.token = ''
        state.isAuthenticated = false
      }
    },
    setToken(state, token){
      state.token = token
      state.isAuthenticated = true
    },
    removeToken(state){
      state.token= ''
      state.isAuthenticated = false
    },
    getUser(state,id){
      state.user = id
    },

    allUsers(state,arr){
      state.users = arr
    },

    removeUsers(state){
      state.user = []
      state.users = []
    }
  },
  actions: {
    async getUser(ctx) {
      await axios.get('api/auth/users/me')
          .then((response) => {
             let userId = (response.data)
            ctx.commit('getUser', userId)
          });
    },

    async loadUsers(ctx) {
      this.users = await axios
          .get('api/users/'
          ).then((response) => {
            let users = (response.data)
            ctx.commit('allUsers', users)
          });
    },

  },
  modules: {

  },
  getters : {
    isLoggedIn: state => !!state.token,
    authStatus: state => state.status,

    getServerUrl: state => {
      return state.backendUrl
    },

    getUsers: state => {
      return state.user
    },

    getAllUsers: state => {
      return state.users
    },

  }
})
