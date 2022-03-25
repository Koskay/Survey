<template>
  <div class="main">
    <b-row>
    <div class="item mt-4 p-2" v-for="sur in surveyList" :key="sur.id">
      <div v-if="sur.s_types===1">
        <h2 style="font-weight:bold">Тест</h2>
          <b-button @click="validateUserOnStaff" v-b-toggle="`collapse-${sur.id}`">{{ sur.sur_name }}</b-button>
          <b-collapse :id="`collapse-${sur.id}`">
            <b-card class="m-2">
              <div v-if="filteredList(sur.start) > today">
                <h2>Тест еще не начался!</h2>
                <h3>Начало: {{sur.start}}</h3>
              </div>
              <div v-else-if="filteredList(sur.finish) < today">
                <h2>Тест Закончился!</h2>
                <h3>Окончание: {{sur.finish}}</h3>
                <div v-if="userStaff">
                  <b-button size="sm"  @click="goToStatic(sur.id)">Посмотреть статистику</b-button>
                </div>
              </div>
              <div v-else>
                <div v-if="userStaff">
                  <b-button  size="sm"  href="#" @click="goToQuest(sur.id)">Пройти тест</b-button>
                  <b-button href="#" size="sm"  @click="goToStatic(sur.id)">Посмотреть статистику</b-button>
                </div>
                <div v-else>
                  <b-button href="#" size="sm"   @click="goToQuest(sur.id)">Пройти тест</b-button>
                </div>
              </div>
            </b-card>
          </b-collapse>
        </div>
      <div v-else>
        <h2 style="font-weight:bold">Опрос</h2>
        <b-button @click="validateUserOnStaff"   v-b-toggle="`collapse-${sur.id}`" >{{ sur.sur_name }}</b-button>
        <b-collapse  :id="`collapse-${sur.id}`">
          <b-card class="m-2">
            <div v-if="filteredList(sur.start) > today">
              <h2>Опрос еще не начался!</h2>
              <h3>Начало: {{sur.start}}</h3>
            </div>
            <div v-else-if="filteredList(sur.finish) < today">
              <h2>Опрос Закончился!</h2>
              <h3>Окончание: {{sur.finish}}</h3>
              <div v-if="userStaff">
                <b-button size="sm"  @click="goToStatic(sur.id)">Посмотреть статистику</b-button>
              </div>
            </div>
            <div v-else>
              <div v-if="userStaff">
                <b-button  size="sm"  @click="goToQuest(sur.id)">Пройти опрос</b-button>
                <b-button size="sm"  @click="goToStatic(sur.id)">Посмотреть статистику</b-button>
              </div>
              <div v-else>
                <b-button size="sm"  @click="goToQuest(sur.id)">Пройти опрос</b-button>
              </div>
            </div>
          </b-card>
        </b-collapse>
      </div>
    </div>
    </b-row>
  </div>
</template>

<script>
import axios from "axios";
import {mapGetters} from "vuex";


export default {

  name: "Survey",

  data() {
    return {
      surveyList: [],
      userStaff: false,
      today : null,
    }
  },

  computed: mapGetters(['getAllUsers', 'getUsers']),

  created() {
    this.loadSurvey()
    this.getDateNow()
    this.$store.dispatch('getUser')
    this.$store.dispatch('loadUsers')
  },


  methods: {
    async loadSurvey() {
      this.surveyList = await axios
      
      .get('api/surveyList/'
      ).then(response => response.data)
    },

    goToQuest(id) {
      this.$router.push({name: 'Questions', params: {'id': id}})
    },

    goToStatic(id) {
      this.$router.push({name: 'Statistic', params: {'id': id}})
    },

    validateUserOnStaff() {
      for (let user of this.getAllUsers) {
        if (user.id === this.getUsers.id && user.is_staff){
          this.userStaff = true
        }
      }
    },

    getDateNow() {
      let now = Date.now()
      this.today = new Date(now)
    },

    filteredList(str) {
      return  new Date(str)
    },


  }


}
</script>

<style scoped>


</style>