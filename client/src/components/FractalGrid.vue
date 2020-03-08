<template>
<div class="wrapper">
<div class="gallery" id="gallery">
        <div v-for="(img, i) in galleryImgs" class="gallery-item">
            <div class="content" @click="openGalleryImg(img)">
                <img :style="getHeight(i)" :src='getImgData(img)' alt="">
            </div>
        </div>
    </div>
</div>

</template>

<script>
import { mapState, mapActions, mapMutations } from 'vuex';
    export default {
        name: "fractalGrid",
        props: ["galleryImgs"],
        watch: {
            galleryImgs() {
                this.reshapeGallery();
            }
        },
        data() {
            return {
                faceImageBG: "",
                imagesLen: 16
            }
        },
        methods: {
            ... mapActions('socketStore', [
                'sendEditAction'
            ]),
            getImgData(i) {
                if(i.png) {
                    let base64Png = "data:image/jpeg;charset=utf-8;base64,"+i.png;
                    return base64Png;
                } else {
                    return "https://swap-samples.s3-us-west-2.amazonaws.com/resImg.jpg";
                }
            },
            resizeAll() {
                console.log("resizeAll");
            },
            getHeight(i) {
                let height = 400;
                if(i % 2 == 0) height = 300;
                let style = "height: " + height + "px"; //+ ", width: 200px}";
                return style;
            },
            reshapeGallery(){
                var getVal = function (elem, style) { return parseInt(window.getComputedStyle(elem).getPropertyValue(style)); };
                var getHeight = function (item) { return item.querySelector('.content').getBoundingClientRect().height; };
                var gallery = document.querySelector('#gallery');
                gallery.querySelectorAll('img').forEach(function (item) {
                  item.addEventListener('load', function () {
                      var altura = getVal(gallery, 'grid-auto-rows');
                      var gap = getVal(gallery, 'grid-row-gap');
                      var gitem = item.parentElement.parentElement;
                      var spanend = Math.ceil((getHeight(gitem) + gap) / (altura + gap));
                      gitem.style.gridRowEnd = "span " + spanend;
                  })
                });
            },
            openGalleryImg(img) {
              let msg = {};
              msg.action = "loadGalleryImg";
              msg.params = {"galleryIdx": img.galleryIdx};
              this.sendEditAction(msg);
              this.$router.push("/");
            }
        },
        mounted() {
            var img = 'url("./resImg.jpg")';
            this.faceImageBG = img;
            var getVal = function (elem, style) { return parseInt(window.getComputedStyle(elem).getPropertyValue(style)); };
            var getHeight = function (item) { return item.querySelector('.content').getBoundingClientRect().height; };
            var gallery = document.querySelector('#gallery');
            var resizeAll = function () {
                var altura = getVal(gallery, 'grid-auto-rows');
                var gap = getVal(gallery, 'grid-row-gap');
                gallery.querySelectorAll('.gallery-item').forEach(function (item) {
                    var el = item;
                    el.style.gridRowEnd = "span " + Math.ceil((getHeight(item) + gap) / (altura + gap));
                });
            };
            gallery.querySelectorAll('img').forEach(function (item) {
                item.addEventListener('load', function () {
                    var altura = getVal(gallery, 'grid-auto-rows');
                    var gap = getVal(gallery, 'grid-row-gap');
                    var gitem = item.parentElement.parentElement;
                    var spanend = Math.ceil((getHeight(gitem) + gap) / (altura + gap));
                    gitem.style.gridRowEnd = "span " + spanend;
                })
            })
            window.addEventListener('resize', resizeAll);
        }
    }
</script>

<style lang="scss" scoped>
.gallery {
  display: grid;
  width: 100vw;
  grid-column-gap: 8px;
  grid-row-gap: 8px;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  grid-auto-rows: 8px;
}
.gallery img {
  max-width: 100%;
  border-radius: 8px;
  box-shadow: 0 0 16px #333;
  transition: all 1.5s ease;
}
.gallery img:hover {
  box-shadow: 0 0 32px #333;
}
.gallery .content {
  padding: 4px;
}
.gallery .gallery-item {
  transition: grid-row-start 300ms linear;
  transition: transform 300ms ease;
  transition: all 0.5s ease;
  cursor: pointer;
}
.gallery .gallery-item:hover {
  transform: scale(1.025);
}
@media (max-width: 600px) {
  .gallery {
    grid-template-columns: repeat(auto-fill, minmax(30%, 1fr));
  }
}
@media (max-width: 400px) {
  .gallery {
    grid-template-columns: repeat(auto-fill, minmax(50%, 1fr));
  }
}
</style>