<template>
<div class="wrapper">
    <div class="main-head"><logoHeading></logoHeading></div>
    <div class="galleryWrapper">
        <fractalGrid :galleryImgs="galleryImgs"></fractalGrid>
    </div>
</div>
</template>
<script>
import fractalGrid from '@/components/FractalGrid.vue';
import logoHeading from '@/components/LogoHeading.vue';
import { mapState, mapActions, mapMutations } from 'vuex'
    export default {
        name: "GalleryMobile",
        components: {
            fractalGrid: fractalGrid,
            logoHeading: logoHeading,
        },
        computed: mapState({
            galleryImgs_store: state => state.socketStore.galleryImgs
        }),
        watch: {
            galleryImgs_store:  {
                handler: function(n, o) {
                    this.loadGallery(n);
                },
                deep: true,
                immediate: true
            }
        },
        data() {
            return {
                galleryImgs: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
            }
        },
        mounted() {
        },
        methods: {
            loadGallery(imgArr) {
                if(imgArr == null) return;
                this.galleryImgs = imgArr;
            },
        }
    }
</script>

<style lang="scss" scoped>
</style>