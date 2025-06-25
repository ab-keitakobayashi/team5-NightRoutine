import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";
import router from "./router";

// Vuetify
import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
//下記の赤線は無視
import "vuetify/styles";
import "@mdi/font/css/materialdesignicons.css";
import VCalendar from "v-calendar";
import "v-calendar/style.css";

const vuetify = createVuetify({
  components,
  directives,
});

const app = createApp(App);
app.use(vuetify);
app.use(VCalendar, {
  componentPrefix: "vc",
});
app.use(router);
app.mount("#app");
