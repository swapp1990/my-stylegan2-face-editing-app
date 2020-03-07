<template>
    <div class="wrapper">
        <div class="item1 thinScroll">
            <checkbox-picker :initMax="5" v-on:checked="onMixLayerPicked"></checkbox-picker>
        </div>
        <div class="item2 thinScroll">
            <scroll-gallery :mixImgs="galleryMixImgs" @onMiximgClick="onMiximgClick"></scroll-gallery>
        </div>
    </div>
</template>

<script>
import scrollGallery from '@/components/VerticalScrollImg.vue';
import checkboxPicker from '@/components/CheckboxPicker.vue';
    export default {
        name:"stylemixMenu",
        components: {
            checkboxPicker: checkboxPicker,
            scrollGallery: scrollGallery
        },
        data() {
            return {
                galleryMixImgs: ["1", "2", "3", "4", "5"],
                layersMixMap: [],
                selectedImgIdx: 0
            }
        },
        methods: {
            onMiximgClick(imgIdx) {
                this.selectedImgIdx = imgIdx;
                // let params = {"styleImgIdx": imgIdx, "layersMixMap": this.layersMixMap};
                // this.sendEditAction("mixStyleImg", params);
            },
            onMixLayerPicked(vals) {
                this.layersMixMap = vals;
                let params = {"styleImgIdx": this.selectedImgIdx, "layersMixMap": this.layersMixMap};
                // this.sendEditAction("mixStyleImg", params);
            },
        }
    }
</script>

<style lang="scss" scoped>
$red: #d30320;
.wrapper {
    height: inherit;
    display: grid;
    grid-template-columns: 0.3fr 0.7fr;
    grid-gap: 5px;
    grid-auto-rows: auto;
    grid-template-areas: 
        "a b b";
    .item1 {
        grid-area: a;
        overflow-y: scroll;
        overflow-x: hidden;
        height: inherit;
    }
    .item2 {
        grid-area: b;
        overflow-y: scroll;
        height: inherit;
    }
}
.thinScroll::-webkit-scrollbar-track {
    -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.3);
	border-radius: 10px;
	background-color: #F5F5F5;
}
.thinScroll::-webkit-scrollbar
{
	width: 5px;
	background-color: #F5F5F5;
}
.thinScroll::-webkit-scrollbar-thumb
{
	-webkit-box-shadow: inset 0 0 6px rgba(0,0,0,.3);
	background-color: rgba($red, .55);
}
</style>