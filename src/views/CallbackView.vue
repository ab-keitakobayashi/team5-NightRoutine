<template>
  <v-container class="d-flex align-center justify-center" style="height: 100vh">
    <v-row class="ma-0 pa-0">
      <v-col cols="12" class="text-center">
        <p>リダイレクト中...</p>
      </v-col>
    </v-row>
  </v-container>
</template>
<script setup lang="ts">
import { useRoute } from "vue-router";
import axios from "axios";
import { jwtDecode } from "jwt-decode"; // npm install jwt-decode
import { useRouter } from "vue-router";
import { onMounted } from "vue";
const router = useRouter();
const route = useRoute();
onMounted(async () => {
  const token = route.query.code;
  if (!token) {
    router.push("/login");
    return;
  }

  const clientId = "4qfsnitgm7uc023mv5icdq04i0";
  const redirectUri = "http://localhost:5173/callback";
  const tokenEndpoint =
    "https://ap-southeast-2ngijy9ne3.auth.ap-southeast-2.amazoncognito.com/oauth2/token";
  const params = new URLSearchParams();

  params.append("grant_type", "authorization_code");
  params.append("client_id", clientId);
  params.append("code", token as string);
  params.append("redirect_uri", redirectUri);

  try {
    const res = await axios.post(tokenEndpoint, params, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });

    type CognitoIdTokenPayload = {
      email?: string;
      sub?: string;
      [key: string]: any;
    };
    const id_token = res.data.id_token;
    const userInfo = jwtDecode(id_token) as CognitoIdTokenPayload;
    const email = userInfo.email ?? "";
    const userId = userInfo.sub ?? "";

    localStorage.setItem("user_email", email);
    localStorage.setItem("user_id", userId);

    router.push("/");
    console.log("メールアドレス", email);
    console.log("ユーザーID", userId);
    console.log("ユーザー情報", userInfo);
  } catch (e) {
    alert("認証に失敗しました");
    router.push("/login");
  }
});
</script>
