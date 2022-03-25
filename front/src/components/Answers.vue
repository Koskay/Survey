<template>
  <div class="clickInput" ref="succes">
    <div v-for="(answer, i) in answersList" :key="i">
      <div :id="answer.id" v-if="questionId === answer.question" class="p-1 chek">
        <input :id="answer.input_name" class="m-2 form-check-input" v-model="answers_id"  :value="answer.id" type="checkbox"
               :state="state">
        <label :for="answer.input_name">{{ answer.input_name }}</label>
      </div>
    </div>
    <b-form-invalid-feedback class="fail" :state="state">Выбрано {{ answers_id.length }} из {{count}}</b-form-invalid-feedback>
    <b-button href="#" class="mb-4" :id="questionId" @click="addAnswer">Ответить</b-button>
  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "Answers",
  props: ['questionId'],


  data() {
    return {
      answersList: [],
      answers_id: [],
      count: 0
    }
  },

  created() {
    this.loadAnswers()
    this.$store.dispatch('getUser')
    this.answersPossible()
  },



  computed: {
    state() {
      return this.answers_id.length === this.count
    },
  },

  methods: {
    async loadAnswers() {
      this.answersList = await axios
          .get('api/answers/'
          ).then(response => response.data)
          this.answersPossible()

    },

    addAnswer() {
      this.inputAnswer()
      let data = {
        question_id: this.questionId,
        answer_id: this.answers_id,
        user: this.$store.getters.getUsers.id
      }
      axios
          .post('api/user-answers/', data
          ).then(response => console.log(response.status)
          )
          .catch(err => console.log(err))
    },


    answersPossible() {
      for (let ans of this.answersList) {
        if(ans.question === this.questionId){
          if (ans.possible_answer===1){
            this.count+=1
          }
        }
      }
    },

    inputAnswer() {
      this.$refs.succes.outerHTML = '<h3 class="alert-heading" style="color:#c9fa69; margin-bottom:20px;">Ответ принят!</h3>'
    },
  },
}
</script>

<style scoped>

.fail {
  font-size: 16px;
  font-weight: 600;
  margin-top: 10px;
  margin-bottom: 10px;
  color: #EB5BB1;
}

.chek {
  display: inline-flex;
  align-items: center;
  justify-content: space-between;
  width: 140px;

}

label {
  display: inline-block; 
  width: 100px; 
  text-align: left;
}

.form-check-input:checked{
  background-color: #223951;
  border-color: #c9fa69;
}

.form-check-input:focus {
  box-shadow: 0px 0px 5px 5px #c9fa69;
}

</style>