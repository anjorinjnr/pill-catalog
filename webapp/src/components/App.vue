<template>
  <main class="main" data-ma-theme="green">
    <app-header></app-header>
    <sidebar>  </sidebar>
    <app-content-wrapper></app-content-wrapper>
  </main>
  </template>

</template>

<script>
import Header from './Header'
import AppViewContainer from './AppViewContainer'
import Sidebar from './Sidebar'
export default {
  components: {
    Sidebar,
    'app-header': Header,
    'app-content-wrapper': AppViewContainer
  }
}

</script>
<style src="../assets/css/app.css"></style>