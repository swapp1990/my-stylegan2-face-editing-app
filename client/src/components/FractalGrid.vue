<template>
    <div class="fg-container">
        <section class="grid-layout">
            <figure v-for="i in galleryImgs" class="grid-item">
                <img :src='getImgData(i)' alt="">
                <!-- <div class="gridImg" v-bind:style="{ 'background-image': faceImageBG}"></div> -->
            </figure>

        </section>
    </div>
</template>

<script>
    export default {
        name: "fractalGrid",
        props: ["galleryImgs"],
        watch: {
            galleryImgs() {
                // console.log(this.galleryImgs);
            }
        },
        data() {
            return {
                faceImageBG: "",
                imagesLen: 16
            }
        },
        methods: {
            getImgData(i) {
                let base64Png = "data:image/jpeg;charset=utf-8;base64,"+i.png;
                return base64Png;
            },
        },
        mounted() {
            var img = 'url("./resImg.jpg")';
            this.faceImageBG = img;
        }
    }
</script>

<style lang="scss" scoped>
@import url('https://fonts.googleapis.com/css?family=Marvel:400,700');
/* ========= VARIABLES ========= */
:root {
  --main-color: #ed1c24;
  --border-width: .24vw;
  --gutter: 2vw;
}
.fg-container {
    background-color: #1b1b1b;
}
.grid-layout {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    grid-gap: 10px;
    // grid-auto-rows: minmax(150px, auto);
    grid-auto-flow: dense;
    padding: 10px;

    .grid-item {
        padding: 0.5rem;
        color: #929796;
        background-color: #333;
        border-radius: 5px;

        img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
    }

    .grid-item:nth-child(2n+1) {
        grid-column-end: span 2;
        grid-row-end: span 2;
    }
}
@media (max-width: 600px) {
  .grid-item {
    // grid-column: auto!important;
    // grid-row: auto!important;
  }
}
</style>