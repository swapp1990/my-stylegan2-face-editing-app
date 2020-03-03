<template>
    <div class="galleryGrid">
        <fractalGrid :galleryImgs="galleryImgs"></fractalGrid>
    </div>
</template>

<script>
import fractalGrid from '@/components/FractalGrid.vue';
    export default {
        name:"Gallery",
        components: {
            fractalGrid: fractalGrid,
        },
        mounted() {
            this.getGalleryImgs();
        },
        data() {
            return {
                galleryImgs: [],
            }
        },
        methods: {
            getGalleryImgs() {
                
            }
        }
    }
</script>

<style lang="scss" scoped>
$radius: 3px;
$white: #ffffff;
$dark: #DFE4EA;
$shadow-tl: -4px -2px 4px 0px;
$shadow-br: 4px 2px 6px 0px;
$shadow: $shadow-tl $white, $shadow-br $dark;
.galleryGrid {
    background-color: #f5f6f7;
    height: 100%;
    width: 100%;
    padding: 1rem 1.5rem;
    border-radius: $radius;
    box-shadow: $shadow;
}
</style>