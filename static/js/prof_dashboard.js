function serviceHandler(service_uid, s_status) {
    fetch(`/prof/service/${service_uid}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            service_uid: service_uid,
            status: s_status,
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.m == "success") {
            window.location.href = "/prof/dashboard"
        }
    })
}

