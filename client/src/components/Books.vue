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
                  <button
                    type="button"
                    class="btn btn-warning btn-sm"
                    v-b-modal.book-update-modal
                    @click="editBook(book)"
                  >
                    Update
                  </button>
                  <button
                    type="button"
                    class="btn btn-danger btn-sm"
                    @click="deleteBook(book)"
                  >
                    Delete
                  </button>
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

    <!-- TODO: Move to UpdateModal Component -->
    <update-book-modal
      id="book-update-modal"
    >
      <b-modal ref="editBookModal"
        id="book-update-modal"
        title="Update"
        hide-footer
      >
        <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
          <b-form-group
            id="form-title-edit-group"
            label="Title:"
            label-for="form-title-edit-input"
          >
            <b-form-input
              id="form-title-edit-input"
              type="text"
              v-model="editForm.title"
              required
              placeholder="Enter title"
            >
            </b-form-input>
          </b-form-group>

          <b-form-group
            id="form-author-edit-group"
            label="Author:"
            label-for="form-author-edit-input"
          >
            <b-form-input
              id="form-author-edit-input"
              type="text"
              v-model="editForm.author"
              required
              placeholder="Enter author"
            >
            </b-form-input>
          </b-form-group>

          <b-form-group
            id="form-read-edit-group"
          >
            <b-form-checkbox-group
              v-model="editForm.read"
              id="form-checks"
            >
              <b-form-checkbox value="true">Read?</b-form-checkbox>
            </b-form-checkbox-group>
          </b-form-group>

          <b-button-group>
            <b-button type="submit" variant="primary">Update</b-button>
            <b-button type="reset" variant="danger">Cancel</b-button>
          </b-button-group>

        </b-form>
      </b-modal>
    </update-book-modal>

  </b-container>
</template>

<script>
import globalAxios from 'axios';
import Alert from './Alert.vue';
import UpdateBookModal from './UpdateBookModal.vue';

export default {
  data() {
    // TODO: change `read` to a boolean not array
    return {
      addBookForm: {
        title: '',
        author: '',
        read: [],
      },
      books: [],
      showAlert: false,
      message: '',
      editForm: {
        id: '',
        title: '',
        author: '',
        read: [],
      },
    };
  },

  components: {
    'app-alert': Alert,
    'update-book-modal': UpdateBookModal,
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
      if (this.$refs.addBookModal) {
        this.addBookForm.title = '';
        this.addBookForm.author = '';
        this.addBookForm.read = [];
      }
      this.editForm.title = '';
      this.editForm.author = '';
      this.editForm.read = [];
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
      // Todo: check if book already exists
      // Todo: get book title
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

    editBook(book) {
      this.editForm = book;
    },

    onSubmitUpdate(e) {
      e.preventDefault();
      this.$refs.editBookModal.hide();
      let read = false;
      if (this.editForm.read[0]) read = true;
      const payload = {
        title: this.editForm.title,
        author: this.editForm.author,
        read,
      };
      this.updateBook(payload, this.editForm.id);
    },

    updateBook(payload, bookId) {
      // Todo: get book title
      globalAxios.put(`/books/${bookId}`, payload).then((response) => {
        // eslint-disable-next-line
        console.log('response: ', response);
        this.getBooks();
        this.showAlert = true;
        this.message = 'Book updated!';
      }).catch((error) => {
        // eslint-disable-next-line
        console.error(error);
        this.getBooks();
        this.showAlert = true;
        this.message = 'An error occurred whilst updating this book. Please try again.';
      });
    },

    onResetUpdate(e) {
      e.preventDefault();
      this.$refs.editBookModal.hide();
      this.initForm();
      this.getBooks();
    },

    removeBook(bookId) {
      // Todo: get book title
      // Todo: probably add a confirmation modal before book is deleted instead of deleting on button click?
      globalAxios.delete(`/books/${bookId}`).then(() => {
        this.getBooks();
        this.showAlert = true;
        this.message = 'Book deleted!';
      }).catch((error) => {
        // eslint-disable-next-line
        console.error(error);
        this.getBooks();
        this.showAlert = true;
        this.message = 'An error occurred whilst deleting this book. Please try again.';
      });
    },

    deleteBook(book) {
      this.removeBook(book.id);
    },
  },

  created() {
    this.getBooks();
  },

};
</script>

<style scoped></style>
