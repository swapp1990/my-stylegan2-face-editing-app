<template>
    <div class="feed">
        <div v-for='post in posts'>
            <div class="post">
                <div class="header level">
                    <div class='level-left'>
                        <figure class="image is-32x32">
                            <img :src='post.userImage'>
                        </figure>
                        <span class="username">{{post.username}}</span>
                    </div>
                </div>
                <div class='image-container'
                    :style="{ backgroundImage: 'url(' + post.postImage + ')' }">
                </div>
                <div class="content">
                    <div class="heart">
                        <i class="far fa-heart fa-lg" @click='like'></i>
                    </div>
                    <p class='likes'>{{post.likes}} likes</p>
                    <p class='caption'><span>{{post.username}}</span> {{post.caption}}</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        props: ['posts'],
        methods: {
            like() {
                
            }
        },
    }
</script>

<style lang="scss" scoped>
.feed {
  height: 100%;
  overflow-y: scroll;
  overflow-x: hidden;
  margin-right: -15px;
  font-family: "Roboto", sans-serif;
}
.post {
    padding: 5px 0;
    .header {
        height: 30px;
        border-bottom: 1px solid #fff;
        .image {
            display: inline-block;
        }
        img {
            border-radius: 99px;
        }
        .username {
            position: relative;
            top:3px;
            padding-left: 5px;
            font-size: 0.9rem;
            font-weight: bold;
        }
    }
    .level {
        margin-bottom: 0.5rem !important;
    }
    .image-container {
        height: 330px;
        background-repeat: no-repeat;
        background-position: center center;
        background-size: cover;
    }
    .content {
        margin: 7.5px 10px;
    }
    .far.fa-heart, .fas.fa-heart {
        cursor: pointer;
    }
    .likes {
        margin: 5px 0;
        margin-bottom: 5px !important;
        font-size: 0.85rem;
        font-weight: bold;
    }
    .caption {
        font-size: 0.85rem;

        span {
        font-weight: bold;
        }
    }
}
// .post:last-child {
//     margin-bottom: 80px;
// }

</style>