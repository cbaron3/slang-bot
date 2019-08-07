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
              <td>{{ book.title }}</td>
              <td>{{ book.url }}</td>
              <td>
                <span v-if="book.example">Yes</span>
                <span v-else>No</span>
              </td>
              <td>foo</td>
              <td>foo</td>
              <td>foo</td>
              <td>foo</td>
              <td>foo</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      books: [],
    };
  },
  methods: {
    getBooks() {
      const path = 'http://localhost:5000';
      axios.get(path)
        .then((res) => {
          this.books = res.data.books;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getBooks();
  },
};
</script>
