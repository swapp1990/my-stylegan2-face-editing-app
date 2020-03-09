//initial state
const state = {
    username: 'anon',
    isConnected: false,
    socket: null,
    mainFaceImg: null,
    count: 1,
    galleryImgs: null,
    galleryMixImgs: null,
    isMixedLocked: true,
    cleared: null
}

// getters
const getters = {

}

function handleGeneralMsg(content, commit) {
    if(content.action) {
        if(content.action == "sendImg") {
            handleReceivedImg(content, commit);
        } else if(content.action == "sendGallery") {
            handleReceivedGallery(content, commit);
        }
    }
}

function handleReceivedImg(content, commit) {
    content.fig.axes.forEach(a => {
        var base64Data = a.images[0].data;
        var img = "url('data:image/png;base64, "+base64Data + "')";
        commit('setMainFaceImg', img);
    });
}

function handleReceivedGallery(content, commit) {
    if(content.tag.includes("styleMixGallery")) {
        let galleryMixImgs = [];
        content.gallery.forEach(gi => {
            let galleryImg = {};
            galleryImg.galleryIdx = gi.id;
            gi.mp_fig.axes.forEach(a => {
                var base64Data = a.images[0].data;
                galleryImg.png = base64Data;
            });
            galleryMixImgs.push(galleryImg);
        });
        commit('setGalleryMixImgs', galleryMixImgs);
    } else if(content.tag === "gallery") {
        let galleryImgs = [];
        content.gallery.forEach(gi => {
            let galleryImg = {};
            galleryImg.galleryIdx = gi.id;
            gi.mp_fig.axes.forEach(a => {
                var base64Data = a.images[0].data;
                galleryImg.png = base64Data;
            });
            galleryImgs.push(galleryImg);
        });
        commit('setGalleryImgs', galleryImgs);
    }
}

// actions
const actions = {
    connectServer({commit, state}, config) {
        console.log("connecting server");
        let SERVER_URL = "34.214.173.193";
        // SERVER_URL = "localhost"
        let socket = io.connect(SERVER_URL+':5000');
        socket.on('connect',()=>{
            console.log("connected");
            commit('setSocket', socket);
            socket.emit('set-session', {"user": state.username});
            state.isConnected = true
        });
        socket.on('loggedin', (data)=>{
            console.log("logged in ", data);
        });
        socket.on('General',(content)=>{
            console.log('General ', content.action);
            handleGeneralMsg(content, commit);
        });
    },
    sendEditAction({commit, state}, msg) {
        if(state.socket) {
            state.socket.emit('editAction', msg);
        }
    },
    clearStore({commit, state}) {
        state.cleared = true;
    }
}

// mutations
const mutations = {
    setSocket (state, socket) {
        state.socket = socket;
    },
    setMainFaceImg (state, imgData) {
        state.mainFaceImg = imgData;
    },
    setGalleryMixImgs (state, imgArr) {
        state.galleryMixImgs = imgArr;
    },
    setGalleryImgs(state, imgArr) {
        state.galleryImgs = imgArr;
    },
}

export default {
namespaced: true,
state,
getters,
actions,
mutations
}