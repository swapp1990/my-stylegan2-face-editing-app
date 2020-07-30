<template>
  <div class="wrapper">
    <div>
      <h3 @click="goHome">Beautiful Fake Faces</h3>
      <h5>
        <a href="https://twitter.com/swapp19902" target="_blank">
          Created by @swapp19902
          <i class="fab fa-twitter" aria-hidden="true"></i>
        </a>
      </h5>
    </div>
  </div>
</template>

<script>
export default {
  name: "logoHeading",
  methods: {
    goHome() {
      this.$router.push("/");
    },
  },
};
</script>

<style lang="scss" scoped>
@import url("https://fonts.googleapis.com/css?family=Dancing+Script&display=swap");
.wrapper {
  display: flex;
  flex-direction: column;
}

h3 {
  padding: 0px;
  font-family: "Dancing Script", cursive;
  color: #202020;
  font-size: 50px;
  color: #e9c9a9;
  text-shadow: 0 12px 8.896px #c4b59d, 0 -3px 1px #fff;
  letter-spacing: -4px;
  margin-bottom: 0;
}
h5 {
  font-family: "Open Sans";
  color: #fcefe3;
  text-shadow: 0 2px 8.896px #420b01, 0 -1px 1px rgb(0, 0, 0);
  cursor: pointer;
  font-size: 18px;
  font-weight: normal;
  margin-bottom: 0;
  text-align: center;
}
@media screen and (max-width: 720px) {
  h3 {
    font-size: 40px;
    line-height: 30px;
    margin: 5px 0 8px 0;
    text-shadow: 0 6px 4px #c4b59d, 0 -2px 1px #fff;
  }
  h5 {
    font-size: 13px;
    font-weight: normal;
  }
}
</style>