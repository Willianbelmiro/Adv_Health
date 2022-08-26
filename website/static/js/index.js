function deleteOwner(ownerId){
  fetch('/delete-owner', {
    method: 'POST',
    body: JSON.stringify({ownerId: ownerId}),

  }).then((_res) => {
    window.location.href = "/";
  })
}

function deleteCar(carId, ownerId){
  fetch('/delete-car', {
    method: 'POST',
    body: JSON.stringify({carId: carId}),

  }).then((_res) => {
    window.location.href = "/profile?id="+ownerId;
  })
}

