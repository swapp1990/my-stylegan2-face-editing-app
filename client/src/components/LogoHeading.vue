<template>
<div class="wrapper">
    <h3 @click="goHome"> Beautiful Fake Faces</h3>
</div>
</template>

<script>
    export default {
        name: "logoHeading",
        methods: {
          goHome() {
            this.$router.push('/');
          }
        }
    }
</script>

<style lang="scss" scoped>
@import url('https://fonts.googleapis.com/css?family=Dancing+Script&display=swap');
.wrapper {

}
h3 {
  /* margin: 20px; */
  padding: 0px;
  font-family: 'Dancing Script', cursive;
  color: #202020;
  // text-transform: uppercase;
  letter-spacing: -2px;

  display: block;
//   margin: 11px 0 17px 0;
  font-size: 60px;
//   line-height: 60px;
  color: #e9c9a9;
  text-shadow: 0 12px 8.896px #c4b59d,0 -3px 1px #fff;
  letter-spacing: -4px;
}
@media screen and (max-width:720px) {
h3 {
    font-size: 40px;
    line-height: 30px;
    margin: 5px 0 8px 0;
    text-shadow: 0 6px 4px #c4b59d,0 -2px 1px #fff;
}
}
</style>