//initial state
const state = {
  username: "anon",
  isConnected: false,
  socket: null,
  mainFaceImg: null,
  count: 1,
  galleryImgs: null,
  isGalleryLoading: false,
  receiveGalleryAfterSave: false,
  galleryMixImgs: null,
  chatsArr: [
    { user: "anon", chatTxt: "Hello!" },
    { user: "anon", chatTxt: "How are you?" },
  ],
  isMixedLocked: true,
  cleared: null,
};

// getters
const getters = {};

function handleGeneralMsg(content, commit, state) {
  if (content.action) {
    if (content.action == "sendImg") {
      handleReceivedImg(content, commit);
    } else if (content.action == "sendGallery") {
      handleReceivedGallery(content, commit, state);
    } else if (content.action == "sendGalleryMetadata") {
      handleReceivedGalleryMetadata(content, commit, state);
    } else if (content.action == "gotNewChat") {
      handleChats(content, commit, state);
    }
  }
}

function handleChats(content, commit, state) {
  commit("setChats", content.chats);
  // console.log("gotNewChat ", content.chats);
}

function handleReceivedImg(content, commit, state) {
  content.fig.axes.forEach((a) => {
    var base64Data = a.images[0].data;
    var img = "url('data:image/png;base64, " + base64Data + "')";
    commit("setMainFaceImg", img);
  });
}

function handleReceivedGallery(content, commit, state) {
  if (content.tag.includes("styleMixGallery")) {
    let galleryMixImgs = [];
    content.gallery.forEach((gi) => {
      let galleryImg = {};
      galleryImg.galleryIdx = gi.id;
      gi.mp_fig.axes.forEach((a) => {
        var base64Data = a.images[0].data;
        galleryImg.png = base64Data;
      });
      galleryMixImgs.push(galleryImg);
    });
    commit("setGalleryMixImgs", galleryMixImgs);
  } else if (content.tag === "gallery") {
    let galleryImgs = [];
    state.receiveGalleryAfterSave = true;
    // console.log(content);
    let i = 0;
    content.gallery.forEach((gi) => {
      let galleryImg = {};
      galleryImg.galleryIdx = gi.id;
      gi.mp_fig.axes.forEach((a) => {
        var base64Data = a.images[0].data;
        galleryImg.png = base64Data;
      });
      let metadata = content.metadata[i];
      if (metadata) {
        galleryImg = setMetadata(galleryImg, metadata);
      }
      galleryImgs.push(galleryImg);
      i++;
    });
    galleryImgs.sort((a, b) => (a.lovecount < b.lovecount ? 1 : -1));
    // galleryImgs.sort((a,b) => (a.username != state.username ? 1 : -1))
    commit("setGalleryImgs", galleryImgs);
    state.isGalleryLoading = false;
  }
}

function handleReceivedGalleryMetadata(content, commit, state) {
  // console.log(content.metadata);
  let i = 0;
  state.galleryImgs.forEach((img) => {
    let metadata = content.metadata[i];
    img = setMetadata(img, metadata);
    i++;
  });
}

function setMetadata(img, metadata) {
  img.idx = metadata.idx;
  img.username = metadata.username;
  if (!metadata.totalLoved) {
    img.lovecount = 0;
  } else {
    img.lovecount = metadata.totalLoved;
  }
  if (metadata.isCurrUserLoved) {
    img.loved = true;
  } else {
    img.loved = false;
  }
  return img;
}

// actions
const actions = {
  connectServer({ commit, state }, username) {
    console.log("connecting server");
    // let SERVER_URL = "34.214.173.193";
    let SERVER_URL = "localhost";
    let socket = io.connect(SERVER_URL + ":5000");
    socket.on("connect", () => {
      console.log("connected");
      commit("setSocket", socket);
      state.username = username;
      socket.emit("set-session", { user: state.username });
      state.isConnected = true;
    });
    socket.on("loggedin", (data) => {
      console.log("logged in ", data);
    });
    socket.on("General", (content) => {
      console.log("General ", content.action);
      handleGeneralMsg(content, commit, state);
    });
  },
  sendEditAction({ commit, state }, msg) {
    if (state.socket) {
      if (!msg.username) {
        msg.username = state.username;
      }
      state.socket.emit("editAction", msg);
    }
  },
  sendChatToServer({ commit, state }, msg) {
    if (state.username) {
      let chatMsg = {};
      let params = { user: state.username, chatTxt: msg };
      chatMsg.action = "sendChat";
      chatMsg.params = params;
      if (state.socket) {
        state.socket.emit("chatAction", chatMsg);
      }
      console.log("sendChatToServer", state.username);
    }
  },
  clearStore({ commit, state }) {
    state.cleared = true;
  },
};

// mutations
const mutations = {
  setSocket(state, socket) {
    state.socket = socket;
  },
  setMainFaceImg(state, imgData) {
    state.mainFaceImg = imgData;
  },
  setGalleryMixImgs(state, imgArr) {
    state.galleryMixImgs = imgArr;
  },
  setGalleryImgs(state, imgArr) {
    state.galleryImgs = imgArr;
  },
  setChats(state, chatsArr) {
    state.chatsArr = chatsArr;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
