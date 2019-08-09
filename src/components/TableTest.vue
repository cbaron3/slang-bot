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
              <tr v-for="(book, index) in books" :key="index">
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
import axios from 'axios'

export default {
  data () {
    return {
      books: []
    }
  },
  methods: {
    getBooks () {
      const path = 'http://localhost:5000/table'
      axios.get(path)
        .then((res) => {
          this.books = res.data.books
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        })
    }
  },
  created () {
    this.getBooks()
  }
}
</script>
