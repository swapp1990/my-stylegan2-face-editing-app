<template>
    <div class="parent">
        <div class="gallery">
            <div v-for="img in mixImgs" class="imgRow" @click="setFocus(img.galleryIdx)">
                <img :src='getImgData(img)' alt="" :class="getSelectedCls(img)">
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "scrollGallery",
        props: ["mixImgs", "selectedImgIdx"],
        watch: {
            "selectedImgIdx": {
                handler: function(n, o) {
                    // console.log("selectedImgIdx ", n);
                },
                immediate:true
            }
        },
        methods: {
            getImgData(i) {
                if(i.png) {
                    let base64Png = "data:image/jpeg;charset=utf-8;base64,"+i.png;
                    return base64Png;
                } else {
                    return "https://swap-samples.s3-us-west-2.amazonaws.com/resImg.jpg";
                }
            },
            setFocus(img) {
                this.$emit('onMiximgClick', img);
            },
            getSelectedCls(img) {
                if(img.galleryIdx === this.selectedImgIdx) {
                    return 'selected';
                } else return '';
            }
        }
    }
</script>

<style lang="scss" scoped>
$white: #ffffff;
$dark: #DFE4EA;
$shadow-tl: -4px -2px 4px 0px;
$shadow-br: 4px 2px 6px 0px;
$shadow: $shadow-tl $white, $shadow-br $dark;
$shadow-flip: $shadow-tl $dark inset, $shadow-br $white inset;

.parent {
    // overflow-y: scroll;
    height: 100%;
    .gallery {
        display: grid;
        grid-gap: 15px;
        grid-auto-rows: auto;
        justify-items: center;
        .imgRow {
            cursor: pointer;
            outline: none;
            border: none;
            box-shadow: $shadow;
            &:hover {
                box-shadow: $shadow-flip;
            }
            img {
                margin: 0 auto;
                width: 128px;
                height: 128px;
                background-repeat: no-repeat;
                background-size: auto;
                background-color: black;
                &.selected {
                    border: 3px solid #f31a1ed1;
                    border-radius: 4px;
                }
            }
        }
    }
}
</style>