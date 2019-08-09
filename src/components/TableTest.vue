<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Books</h1>
        <hr>
        <br>
        <div class="intro">
            <p>Subreddit bot</p>
        </div>
        <br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">User</th>
              <th scope="col">Subreddit</th>
              <th scope="col">Created</th>
              <th scope="col">Received</th>
              <th scope="col">URL</th>
              <th scope="col">Word</th>
              <th scope="col">Meaning</th>
              <th scope="col">Example</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <tr v-for="(book, index) in resources" :key="index">
                <td>{{ book.user }}</td>
                <td>{{ book.subreddit }}</td>
                <td>{{ book.created_time }}</td>
                <td>{{ book.received_time }}</td>
                <td>{{ book.url }}</td>
                <td>{{ book.word }}</td>
                <td>{{ book.meaning }}</td>
                <td>{{ book.example }}</td>
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
