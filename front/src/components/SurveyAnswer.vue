<template>
  <div ref="succes">
    <b-form-input class="inp" v-model="answer"  type="text" debounce="200" placeholder="Ваш ответ..."></b-form-input>
    <b-button class="m-4" @click="addAnswer">Отправить</b-button>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: "SurveyAnswer",
  props: ['questionId'],

  data(){
    return {
      answer: '',
    }
  },


  created() {
    this.$store.dispatch('getUser')
  },

  methods: {

    addAnswer() {
      this.inputAnswer()
      let data = {
        question_id: this.questionId,
        user: this.$store.getters.getUsers.id,
        answer_text: this.answer
      }
      axios
          .post('api/user-answer-input/', data
          ).then(response => console.log(response.status)
      )
          .catch(err => console.log(err))
    },

    inputAnswer() {
      this.$refs.succes.outerHTML = '<h3 class="alert-heading" style="color:#c9fa69; margin-bottom:20px;">Спасибо за ответ!</h3>'
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
}

.inp:focus {
  border: 1px solid #c9fa69;
  box-shadow: 0px 0px 5px 2px #c9fa69;
}

</style>