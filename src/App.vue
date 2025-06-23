<template>
  <v-app>
    <header>
      <v-app-bar app color="black" dark>
        <v-btn text to="/">Home</v-btn>
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
    </header>
    <body class="bg-grey lighten-4">
      <v-main>
        <v-container fluid>
          <router-view />
        </v-container>
      </v-main>
    </body>
  </v-app>
</template>

<script setup lang="ts"></script>
<style scoped></style>
