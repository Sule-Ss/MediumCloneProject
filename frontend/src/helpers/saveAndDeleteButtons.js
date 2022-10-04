export const addSavedFunction = (storyId, tokenKey, addSave) => {
  let myHeaders = new Headers();
  myHeaders.append("Authorization", `Token ${tokenKey}`);
  myHeaders.append("Content-Type", "application/json");

  let raw = JSON.stringify({ story: storyId });

  if (addSave) {
    console.log("delete");

    var requestOptions = {
      method: "DELETE",
      headers: myHeaders,
      // body: raw,
      redirect: "follow",
    };

    fetch(`http://127.0.0.1:8000/blog/save/${storyId}/`, requestOptions)
      .then((response) => response.text())
      .then((result) => console.log(result))
      .catch((error) => console.log("error", error));
  } else {
    // console.log("add");

    let requestOptions = {
      method: "POST",
      headers: myHeaders,
      body: raw,
      redirect: "follow",
    };

    fetch("http://127.0.0.1:8000/blog/save/", requestOptions)
      .then((response) => {response.text()})
      .then((result) => console.log(result))
      .catch((error) => console.log("error", error));
  }
};

export const controlFollowFunction = (
  setfollowOrFollowing,
  userId,
  tokenKey
) => {
  let myHeaders = new Headers();
  myHeaders.append("Authorization", `Token ${tokenKey}`);
  myHeaders.append("Content-Type", "application/json");

  let requestOptions = {
    method: "GET",
    headers: myHeaders,
    redirect: "follow",
  };

  fetch("http://127.0.0.1:8000/auth/following/", requestOptions)
    .then((response) => response.json())
    .then((result) => {
      // console.log(result);

      let followedList = [];
      result.results.map((item) => {
        followedList.push(item.followed);
      });

      if (followedList.includes(userId)) {
        setfollowOrFollowing(true);
      } else {
        setfollowOrFollowing(false);
      }
    })
    .catch((error) => console.log("error", error));
};

export const add_deleteFollowHandle = (followOrFollowing, tokenKey, userId, followedUserStories, setFollowingStories ) => {
  let myHeaders = new Headers();
  myHeaders.append("Authorization", `Token ${tokenKey}`);
  myHeaders.append("Content-Type", "application/json");

  if (followOrFollowing) {
    let raw = JSON.stringify({
      followed: userId,
    });

    var requestOptions = {
      method: "DELETE",
      headers: myHeaders,
      body: raw,
      redirect: "follow",
    };

    fetch(`http://127.0.0.1:8000/auth/following/${userId}/`, requestOptions)
      .then((response) => response.text())
      .then((result) => console.log(result))
      .catch((error) => console.log("error", error));
  } else {
    let raw = JSON.stringify({
      followed: userId,
    });

    var requestOptions = {
      method: "POST",
      headers: myHeaders,
      body: raw,
      redirect: "follow",
    };

    fetch("http://127.0.0.1:8000/auth/following/", requestOptions)
      .then((response) => response.text())
      .then((result) => {
        console.log(result)
        followedUserStories(setFollowingStories, tokenKey)
      })
      .catch((error) => console.log("error", error));
  }
};
