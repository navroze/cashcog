function getExpenses(zgRef){
  fetch('http://127.0.0.1:5000/query/')
    .then(res => res.json())
    .then(data => {
      console.log(data.data)
      zgRef.setData(data.data);
    }).catch(error => {
      console.log(error)
    });
}

function approveExpense(zgRef, uuid, status){
  const postData = {
    "uuid": uuid,
    "status": status
  }
  fetch('http://127.0.0.1:5000/validate/', {
      method: 'post',
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(postData)
    }).then(function(response) {
      return response.json();
    }).then(function(data) {
      console.log("data", data);
      return data;
    })
    .then(data => {
      getExpenses(zgRef);
    })
    .catch(error => {
      console.log(error)
    })
}


window.addEventListener('load', () => {
  // Javascript code to execute after DOM content
  const zgRef = document.querySelector('#expenses_table');
    zgRef.executeOnLoad(() => {
      getExpenses(zgRef)
    });

  zgRef.addEventListener('record:click', function(e) {
    console.log('--- (record:click) event fired ---', e.detail.ZGEvent.oDOMTarget.className, e.detail.ZGData.data.uuid);
    const uuid = e.detail.ZGData.data.uuid
    if(e.detail.ZGEvent.oDOMTarget.className === "button is-small is-fullwidth is-primary")
      approveExpense(zgRef, uuid, "approve");
    else if(e.detail.ZGEvent.oDOMTarget.className === "button is-small is-fullwidth is-danger")
      approveExpense(zgRef, uuid, "decline");
  });
});