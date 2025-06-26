<template>
  <v-img src="/assets/bg.png" class="d-flex align-center justify-center">
    <v-row
      align="center"
      justify="center"
      class="ma-0 pa-0"
      style="width: 100%; position: absolute; bottom: 32px; left: 0"
    >
      <v-col cols="3" class="d-flex justify-center mt-5 pt-5">
        <v-btn @click="login" color="grey-lighten-5" block class="pa-7"
          >ログイン</v-btn
        >
      </v-col>
    </v-row>
  </v-img>
</template>

<script setup lang="ts">
async function login() {
  console.log("ログインボタンがクリックされました");

  // Cognitoの認証URL
  const cognitoAuthUrl = "https://ap-southeast-2ngijy9ne3.auth.ap-southeast-2.amazoncognito.com/login?client_id=4qfsnitgm7uc023mv5icdq04i0&response_type=code&scope=openid%20email%20phone&redirect_uri=http%3A%2F%2Flocalhost%3A5173%2Fcallback";

  // リダイレクト
  window.location.href = cognitoAuthUrl;
}
</script>

<style scoped></style>
