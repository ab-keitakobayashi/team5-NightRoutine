import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";

// Vuetify
import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import "vuetify/styles";

const vuetify = createVuetify({
  components,
  directives,
});

createApp(App).mount("#app");

const app = createApp(App);
app.use(vuetify);
app.mount("#app");
