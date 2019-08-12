<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Slang Bot</h1>
        <br>
        <hr>
        <br>
        <div class="intro">
            <p>Frontend to view user requests for <a href='https://github.com/cbaron3/reddit-bot'>Slang Bot</a>, a Reddit Bot that translates slang using Urban Dictionary</p>
            <p>Currently only works on subreddit <a href='https://www.reddit.com/r/testingground4bots/'>testingground4bots</a></p>
        </div>
        <br>
        <hr>
        <br>
        <table class="table table-hover table-borderless">
          <thead>
            <tr>
              <th scope="col">User</th>
              <th scope="col">Subreddit</th>
              <th scope="col">Word</th>
              <th scope="col">URL</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <tr v-for="(book, index) in resources" :key="index">
                <td>{{ book.user }}</td>
                <td>{{ book.subreddit }}</td>
                <td>{{ book.word }}</td>
                <td><a v-bind:href="''">{{ book.url }}</a></td>
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
          this.resources = responseData.books
          console.log('hes')
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
body {
background: #E0EAFC;  /* fallback for old browsers */
background: -webkit-linear-gradient(to right, #CFDEF3, #E0EAFC);  /* Chrome 10-25, Safari 5.1-6 */
background: linear-gradient(to right, #CFDEF3, #E0EAFC); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */

}

h1, p, th, td, hd {
  color: #0074D9;
  font-family: 'Muli', sans-serif;
}

th, td {
  text-align: center;
}

h1 {
  padding-top: 25px;
  font-weight: 700;
  font-size: 4em;
}

p {
  padding-top: 25px;
  font-weight: 500;
  font-size: 1em;
}

</style>
