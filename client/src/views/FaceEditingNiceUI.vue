<template>
<div id='app'>
    <div class='app-phone'>
        <div class='phone-header'>
            <img src='https://s3-us-west-2.amazonaws.com/s.cdpn.io/1211695/vue_gram_logo_cp.png' />
        </div>
        <div class="phone-body">
            <!-- <feed :posts="posts"></feed> -->
            <img v-if="src_face != null" v-bind:src="'data:image/jpeg;base64,'+src_face.data"/>
        </div>
        <div class="phone-footer">
            <div class="home-btn">
                <i class="fas fa-home fa-lg"></i>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import Feed from '@/views/Feed.vue';
    export default {
        name: "FaceEditingUI",
        components: {
            Feed:Feed
        },
        mounted() {
        },
        data() {
            return {
                src_face: null,
                posts: [
                    {
                        username: 'socleansofreshh',
                        userImage: 'https://s3-us-west-2.amazonaws.com/s.cdpn.io/1211695/me_3.jpg',
                        postImage:
                        'https://s3-us-west-2.amazonaws.com/s.cdpn.io/1211695/tropical_beach.jpg',
                        likes: 36,
                        hasBeenLiked: false,
                        caption: 'When you"re ready for summer "18 ☀️',
                        filter: 'perpetua',
                    },
                    {
                        username: 'djirdehh',
                        userImage: 'https://s3-us-west-2.amazonaws.com/s.cdpn.io/1211695/me2.png',
                        postImage:
                        'https://s3-us-west-2.amazonaws.com/s.cdpn.io/1211695/downtown.jpg',
                        likes: 20,
                        hasBeenLiked: false,
                        caption: 'Views from the six...',
                        filter: 'clarendon',
                    },
                    {
                        username: 'puppers',
                        userImage:
                        'https://s3-us-west-2.amazonaws.com/s.cdpn.io/1211695/pug_personal.jpg',
                        postImage:
                        'https://s3-us-west-2.amazonaws.com/s.cdpn.io/1211695/puppers.jpg',
                        likes: 49,
                        hasBeenLiked: false,
                        caption: 'Current mood 🐶',
                        filter: 'lofi',
                    },
                ],
            }
        },
        methods: {
            name() {
                
            }
        },
    }
</script>

<style lang="scss" src='../styles/app.scss'>

</style>