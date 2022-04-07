<template>
  <div>
      <div class="mt-4 question" v-for="question in questionsList" :key="question.id">
        <div v-if="question.types===3">
          <h1 class="mb-4">{{ question.question_name }}</h1>
          <SurveyAnswer v-bind:questionId='question.id'/>
        </div>
        <div v-else>
          <h1>{{ question.question_name }}</h1>
          <div v-if="question.image">
            <img :src="question.image" class="img">
          </div>
          <Answers v-bind:questionId='question.id'/>
        </div>
      </div>
      <div v-if="questions!==3">
        <Results v-bind:survey="id"/>
      </div>
  </div>
</template>

<script>
import Answers from "../components/Answers";
import Results from "@/components/Results";
import axios from "axios"
import SurveyAnswer from "@/components/SurveyAnswer";


export default {
  name: "Questions",
  components: {
    Answers,
    Results,
    SurveyAnswer,
  },
  props: ['id'],


  data() {
    return {
      questionsList: [],
      questions:null,
    }
  },

  created() {
    this.loadQuestions()

  },

  methods: {
    async loadQuestions() {
      this.questionsList = await axios
      .get(`api/questions/${this.id}/`
      ).then(response => response.data)
      this.questions = this.questionsList[0].types
    },
  }
}
</script>

<style scoped>

.question {
  border-bottom:1px solid #c9fa69;
}


.img {
  max-width: 50vw;
  max-height: 40vh;
  margin: 30px;
  border-radius: 14px;
  box-shadow:10px 10px 25px  #c9fa69;
}
</style>