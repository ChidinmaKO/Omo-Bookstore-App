<template>
  <b-container>
    <b-row>
      <b-col col sm="10">
        <h1>Books</h1>
        <hr><br><br>

        <app-alert v-if="showAlert" :message="message"></app-alert>

        <button type="button" class="btn btn-success btn-sm" v-b-modal.book-modal>Add Book</button>
        <br><br>

        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Title</th>
              <th scope="col">Author</th>
              <th scope="col">Read?</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(book, index) in books" :key="`book[0]-${index}`">
              <td>{{ book.title }}</td>
              <td>{{ book.author }}</td>
              <td>
                <span v-if="book.read">Yes</span>
                <span v-else>No</span>
              </td>
              <td>
                <div class="btn-group" role="group">
                  <button type="button" class="btn btn-warning btn-sm">Update</button>
                  <button type="button" class="btn btn-danger btn-sm">Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

      </b-col>
    </b-row>

    <b-modal ref="addBookModal"
      id="book-modal"
      title="Add a new book"
      hide-footer
    >
      <b-form
        @submit="onSubmit"
        @reset="onReset"
        class="w-100"
      >
        <b-form-group
          id="form-title-group"
          label="Title:"
          label-for="form-title-input"
        >
          <b-form-input
            id="form-title-input"
            type="text"
            v-model="addBookForm.title"
            required
            placeholder="Enter title"
          >
          </b-form-input>
        </b-form-group>

        <b-form-group
          id="form-author-group"
          label="Author:"
          label-for="form-author-input"
        >
          <b-form-input
            id="form-author-input"
            type="text"
            v-model="addBookForm.author"
            required
            placeholder="Enter author"
          >
          </b-form-input>
        </b-form-group>

        <b-form-group
          id="form-read-group"
        >
          <b-form-checkbox-group
            v-model="addBookForm.read"
            id="form-checks"
          >
            <b-form-checkbox
              value="true"
            >
              Read?
            </b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>

        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>
  </b-container>
</template>

<script>
import globalAxios from 'axios';
import Alert from './Alert.vue';

export default {
  data() {
    return {
      addBookForm: {
        title: '',
        author: '',
        read: [],
      },
      books: [],
      showAlert: false,
      message: '',
    };
  },

  components: {
    'app-alert': Alert,
  },

  methods: {
    getBooks() {
      globalAxios.get('/books').then((response) => {
        this.books = response.data.books;
      }).catch((error) => {
        // eslint-disable-next-line
        console.error(error)
        this.showAlert = true;
        this.message = 'An error occurred whilst getting this book. Please try again.';
      });
    },

    initForm() {
      this.addBookForm.title = '';
      this.addBookForm.author = '';
      this.addBookForm.read = false;
    },

    onSubmit(e) {
      e.preventDefault();
      this.$refs.addBookModal.hide();
      let read = false;
      if (this.addBookForm.read[0]) read = true;

      const payload = {
        title: this.addBookForm.title,
        author: this.addBookForm.author,
        read,
      };

      this.addBook(payload);
      this.initForm();
    },

    onReset(e) {
      e.preventDefault();
      this.$refs.addBookModal.hide();
      this.initForm();
    },

    addBook(payload) {
      globalAxios.post('/books', payload).then((response) => {
        // eslint-disable-next-line
        console.log('response: ', response);
        this.getBooks();
        this.showAlert = true;
        this.message = 'Book added!';
      }).catch((error) => {
        // eslint-disable-next-line
        console.error(error);
        this.getBooks();
        this.showAlert = true;
        this.message = 'An error occurred whilst adding this book. Please try again.';
      });
    },

    updateBook() {
      this.showAlert = true;
    },

    removeBook() {
      this.showAlert = true;
    },

    deleteBook() {
      // eslint-disable-next-line
      console.log('book deleted');
    },
  },

  created() {
    this.getBooks();
  },

};
</script>

<style scoped></style>
