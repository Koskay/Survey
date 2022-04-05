<template>
<div>
  <h1 class="mt-3">Статистика</h1>
  <div class="item mt-4 p-2" v-for="(use) in users" :key="use.username">
      <h2>{{use.username}}</h2>
      <b-button  v-b-toggle="`collapse-${use.id}`">Открыть</b-button>
        <b-collapse :id="`collapse-${use.id}`">
          <b-card class="m-2">
            <div>
              <div v-for="(item,i) in statisticList" :key="i">
                <div v-if="use.username===item.user && item.answer_text">
                  <div class="item-card" v-if="item.answer_text">
                    <h3 class="m-2 quest">{{item.question_id}}</h3>
                    <h4 class="m-2">Ответ:</h4>
                    <p class="m-3">{{item.answer_text}}</p> 
                  </div>
                </div>
              </div>  
            </div>
            <div v-if="!statisticList[0] || statisticList[0].answer_text===null">
              <div v-for="(point) in resultsList" :key="point.user_id">
                <div v-if="point.total!==null">
                  <div class="items-card" v-if="point.user_id === use.id">
                    <h2>Кол-во вопросов: {{ point.questions_count }}</h2>
                    <div class="progress">
                      <div class="progress-bar" role="progressbar" :style="`width: ${progress(point.user_questions_count ,point.questions_count)}%`"
                      :aria-valuenow="progress(point.user_questions_count ,point.questions_count)" 
                      aria-valuemin="0" aria-valuemax="100">{{progress(point.user_questions_count ,point.questions_count)}}%</div>
                    </div>
                    <div class="result">
                      <h3>Отвечено: {{ point.user_questions_count }} из {{ point.questions_count }}</h3>
                    </div>
                    <div class="result">
                      <h2>Правильных ответов:</h2>
                      <h3>{{ point.user_answer_count }} из {{ point.answer_count }}</h3>
                    </div>  
                    <div class="result">  
                      <h2>Баллов набрано:</h2>
                      <h3>{{ point.total }} из {{ point.total_sum }}</h3>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </b-card>
        </b-collapse>    
  </div>
</div>
</template>

<script>
import axios from 'axios'


export default {
  name: "Statistic",

  props: ['id'],

  data(){
    return {
      statisticList: [],
      users: [],
      resultsList: {}
    }
  },

  created() {
    this.loadUsers()
    this.loadStatistic()
    this.loadResults()
    this.$store.dispatch('getUser')
  },

  methods: {

    async loadStatistic() {
      this.statisticList = await axios
          .get(`api/statistic/${this.id}`
          ).then(response => response.data)
    },

    async loadUsers() {
      this.users = await axios
          .get('api/auth/users/'
          ).then(response => response.data)
    },

    async loadResults() {
      this.resultsList = await axios
          .get(`api/user-results/${this.id}`
          ).then(response => response.data)
    },

    progress(user, question){
      let bar = parseInt(user*100/question)
      return Number(bar)
    }

  }
}
</script>

<style scoped>

.item-card {
  border-bottom:1px solid #c9fa69;
  margin-top: 20px;
}

h2{
  margin-top: 20px;
}

h3 {
  padding-bottom: 16px;
  margin-top: 14px;
}

.progress-bar {
  background-color: #c9fa69;
  color: #223951;
  font-weight: bold;
  font-size: 1em;
}

.progress {
  display: flex;
  margin-top: 20px;
  max-width: 70%;
  margin-left: 15%;
  margin-right: 15%;
  box-shadow: 0px 0px 2px 2px #223951;
}

.result {
  border-bottom:1px solid #c9fa69;
}

</style>