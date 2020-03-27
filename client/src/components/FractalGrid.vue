<template>
<div class="wrapper">
  
  <div>
    <div class="loading pl-5">
        <i v-if="galleryLoading" class='fas fa-spinner fa-spin fa-fw'></i> 
    </div>
    <div class="gallery" id="gallery">
        <div v-for="(img, i) in galleryImgs" class="gallery-item">
             <!-- @click="openGalleryImg(img)" -->
            <div class="content">
                <img :style="getHeight(i)" :src='getImgData(img)' alt="">
                <div class="overlayAlways">
                    <div class="menuTop">
                        <div></div>
                        <div>
                            <div class="love">
                                <button @click="onLove(i)">
                                    <i v-if="img.loved" class="fas fa-heart fa-fw"></i>
                                    <i v-if="!img.loved"class="far fa-heart fa-fw"></i>
                                </button>
                                <span>{{img.lovecount}}</span>
                            </div>
                            
                        </div>
                    </div>
                    <div class="menuMid"></div>
                    <div class="menuBtm">
                        <input type="button" :value="img.username" class="header"></input>
                    </div>
                </div>
            </div>
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
        
    },
    data() {
        return {
            faceImageBG: "",
            imagesLen: 16,
            galleryLoading: false
        }
    },
    computed: mapState({
        isConnected: state => state.socketStore.isConnected,
        isGalleryLoading: state => state.socketStore.isGalleryLoading,
        receiveGalleryAfterSave: state => state.socketStore.receiveGalleryAfterSave
    }),
    watch: {
        isConnected: {
            handler: function(n, o) {
                if(n) {
                    this.isGalleryLoading = true;
                }
            },
            deep: true,
            immediate: true
        },
        galleryImgs: {
            handler: function(n, o) {
                if(n) {
                    setTimeout(() => {
                        this.reshapeGallery();
                    }, 1000);
                }
            },
            deep: true,
            immediate: true
        },
        isGalleryLoading: {
            handler: function(n, o) {
                if(n) {
                    console.log("gallery is loading");
                    this.galleryLoading = true;
                } else {
                    this.galleryLoading = false;
                }
            },
            deep: true,
            immediate: true
        }
    },
    methods: {
        ... mapActions('socketStore', [
            'sendEditAction'
        ]),
        onLove(idx) {
            let params = {"action": "love", "idx": idx};
            this.$emit("img-clicked", params);
            this.$forceUpdate();
        },
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
                var altura = getVal(gallery, 'grid-auto-rows');
                var gap = getVal(gallery, 'grid-row-gap');
                var gitem = item.parentElement.parentElement;
                var spanend = Math.ceil((getHeight(gitem) + gap) / (altura + gap));
                gitem.style.gridRowEnd = "span " + spanend;
            });
            // this.isGalleryLoading = false;
        },
        openGalleryImg(img) {
            let msg = {};
            msg.action = "loadGalleryImg";
            msg.params = {"galleryIdx": img.galleryIdx};
            this.sendEditAction(msg);
            this.$router.push("/");
            this.$ga.event('category', 'btnClick', 'openGalleryImg', 1);
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
$color-red: #d30320;
%overlayBtn {
    background: transparent;
    outline: none;
    border: none;
    cursor: pointer;
    &:hover {
        color: darken(rgba($color-red, .95), 8%);
        opacity: 1;
    }
}
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
  position: relative;
}
.overlayAlways {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    height: 100%;
    width: 100%;
    opacity: 1;
    transition: .5s ease;
    display: grid;
    grid-template-rows: 1fr 8fr 1fr;
    grid-template-columns: auto;
    .menuTop {
        align-self: start;
        display: flex;
        align-items: center;
        justify-content: space-between;
        button {
            @extend %overlayBtn;
            font-size: 20px;
            color:$color-red;
        }
        .love {
            display: inline-flex;
            flex-direction: column;
            align-items: center;
            font-size: 14px;
            color:black;
            font-family: 'Dancing Script'
        }
        padding: 3px;
    }
    .menuMid {
        align-self: center;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .menuBtm {
        align-self: center;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 3;
        .header {
            background: rgba(#1e1e1f, 0.7);
            outline: none;
            border: none;
            border-radius: 5rem;
            cursor: pointer;
            // -webkit-transform:rotate(90deg);
            margin: 0 auto;
            height: 20px;
            width: 80px;
            font-size: 15px;
            text-transform: uppercase;
            font-weight: 700;
            color: #e9c9a9;
            font-family: 'Dancing Script'
        }
    }

    .overlayText {
        color: rgb(247, 1, 185);
        font-size: 20px;
        font-weight: 800;
        position: absolute;
        top: 10%;
        left: 10%;
        -webkit-transform: translate(-50%, -50%);
        -ms-transform: translate(-50%, -50%);
        transform: translate(-50%, -50%);
        text-align: center;
    }
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