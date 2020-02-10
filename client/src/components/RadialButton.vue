<template>
    <div class="wrap">
        <a href="#"><div></div></a>
        <a href="#"><div></div></a>
        <a href="#"><div></div></a>
        <a href="#"><div></div></a>
        <a href="#"><div></div></a>
    </div>
</template>

<script>
    export default {
        name: "radial-btn",
    }
</script>

<style lang="scss" scoped>
.wrap {
    // margin:0 auto;
    position:relative;
}
a{
  position: absolute;
  left:0; top:0;
  width:47.5%; height:47.5%;
  overflow:hidden;
  transform:scale(.5) translateZ(0px);
  background:#585247;
}
a div{
  height:100%;
  background-size:cover;
  opacity:.5;
  transition:opacity .5s;
  border-radius:inherit;
}
a:nth-child(1){
  border-radius:40vmin 0 0 0;
  transform-origin: 110% 110%;
  transition:transform .4s .15s;
}
a:nth-child(1) div{
  background-image:url('https://farm3.staticflickr.com/2827/10384422264_d9c7299146.jpg');
}
</style>