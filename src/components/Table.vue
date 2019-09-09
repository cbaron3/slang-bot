<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Slang Bot</h1>
        <br>
        <hr>
        <br>
        <div class="intro">
            <p>This web page can be used to view the requests made by users for <a href='https://github.com/cbaron3/reddit-bot'>Slang Bot</a>, a Reddit Bot that translates slang using Urban Dictionary.</p>
            <br>
            <p>Currently, this bot is active on <a href='https://www.reddit.com/r/testingground4bots/'>/r/testingground4bots</a> for demonstration purposes.</p>
        </div>
        <br>
        <hr>
        <br>
        <table class="table table-hover ">
          <thead>
            <tr>
              <th scope="col">User</th>
              <th scope="col">Subreddit</th>
              <th scope="col">Word</th>
              <th scope="col">Time (UTC)</th>
              <th scope="col">URL</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <tr v-for="(request, index) in resources" :key="index">
                <td>{{ request.user }}</td>
                <td>{{ request.subreddit }}</td>
                <td>{{ request.word }}</td>
                <td>{{ request.time }}</td>
                <td><a v-bind:href="request.url">{{ request.url }}</a></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>

import $backend from '../backend'

export default {
  name: 'TableTest',
  data () {
    return {
      resources: [],
      error: ''
    }
  },
  methods: {
    fetchTableTest () {
      $backend.fetchTableData()
        .then(responseData => {
          console.log(responseData)
          this.resources = responseData.requests
          console.log(this.resources)
        }).catch(error => {
          this.error = error.message
          console.log(this.error)
        })
    }
  },
  created () {
    this.fetchTableTest()
  }
}
</script>

<style>

div{
  font-family: 'Muli', sans-serif;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: center;
  align-items: center;
}

h1, table {
  padding-top: 1em;
  width: 100%;
}

h1 {
  font-size: 4.2em;
}

p {
  font-size: 1.375em;
}

th, td {
  font-size: 1.2em;
}

</style>
