<template>
  <v-app>
    <v-app-bar app color="black" dark>
      <v-btn text to="/">振り返り記入</v-btn>
      <v-btn text to="/reports/calender">カレンダー</v-btn>
      <v-spacer></v-spacer>
      <v-toolbar-title
        class="text-center"
        style="justify-content: center; display: flex"
      >
        NightRoutine
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text to="/login">Login</v-btn>
    </v-app-bar>
    <v-main fluid class="full-width bg-grey-darken-4">
      <v-container>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup lang="ts"></script>
<style scoped>
.full-width {
  width: 100vw;
  padding-right: 0;
  padding-left: 0;
  margin-right: 0;
  margin-left: 0;
}
</style>
