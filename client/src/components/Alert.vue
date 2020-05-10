<template>
  <div class="container">
    <b-alert variant="success" show dismissible>
      {{ message }}
    </b-alert>
  </div>
</template>

<script>
export default {
  name: 'Alert',
  props: ['message'],
};
</script>

<style scoped></style>
