<template>
    <div class="parent">
    <video
        id="my-video"
        class="video-js vjs-theme-city"
        autoplay
        controls
        preload="auto"
        :width="width"
        :height="height"
        poster="MY_VIDEO_POSTER.jpg"
        data-setup="{}"
    >
    <source src="dababy.mp4" type="video/mp4" />
    <!-- <source src="MY_VIDEO.webm" type="video/webm" /> -->
    <p class="vjs-no-js">
      To view this video please enable JavaScript, and consider upgrading to a
      web browser that
      <a href="https://videojs.com/html5-video-support/" target="_blank"
        >supports HTML5 video</a
      >
    </p>
  </video>
    </div>
</template>

<script>
    export default {
        name: "videoPlayer",
        data() {
            return {
                width: 512,
                height: 512
            }
        }
    }
</script>

<style scoped>
.parent {
    margin: 0 auto;
}
</style>