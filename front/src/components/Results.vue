<template>
  <div>
    <b-button class="m2" ref="answer" @click.once="loadResults" v-b-toggle.collapse-2 >Посмотреть результаты</b-button>
      <b-collapse id="collapse-2">
        <b-card>
          <div v-if="resultsList.total_sum!==null">
            <h3>Вы набрали:</h3>
            <h4>{{ resultsList.total }} из {{ resultsList.total_sum }} балла(ов)</h4>
            <b-button href="#" @click="reloadPage">Пройти еще раз</b-button>
          </div>
          <div v-else>
            <h3>Вы ответили на {{resultsList.user_quesion_count}} из {{resultsList.questions_count}} вопроса(ов)</h3>р
          </div>
        </b-card>
      </b-collapse>
  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "Results",

  props: ['survey'],

  data() {
    return{
      resultsList: {}
    }
  },


  methods: {
    async loadResults() {
      this.resultsList = await axios
          .get(`api/results/${this.survey}/`
          ).then(response => response.data)
    },

    reloadPage() {
      window.location.reload();
    },
  }
}
</script>

<style scoped>

</style>