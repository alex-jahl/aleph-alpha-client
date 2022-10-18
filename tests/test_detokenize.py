import pytest
from aleph_alpha_client.aleph_alpha_client import AlephAlphaClient
from aleph_alpha_client.aleph_alpha_model import AlephAlphaModel
from aleph_alpha_client.detokenization import DetokenizationRequest

from tests.common import client, model_name, model, checkpoint_name


@pytest.mark.needs_api
def test_detokenize(model: AlephAlphaModel):
    response = model.detokenize(DetokenizationRequest([4711]))

    assert response.result is not None


@pytest.mark.needs_api
def test_detokenize_against_checkpoint(client: AlephAlphaClient, checkpoint_name):
    model = AlephAlphaModel(client, model_name=None, checkpoint_name=checkpoint_name)
    response = model.detokenize(DetokenizationRequest([4711]))

    assert response.result is not None


@pytest.mark.needs_api
def test_detokenize_with_client(client: AlephAlphaClient, model_name: str):
    response = client.detokenize(model_name, token_ids=[4711, 42])

    assert response["result"] is not None


@pytest.mark.needs_api
def test_detokenize_with_client_against_checkpoint(
    client: AlephAlphaClient, checkpoint_name: str
):
    response = client.detokenize(
        model=None, checkpoint=checkpoint_name, token_ids=[4711, 42]
    )

    assert response["result"] is not None


@pytest.mark.needs_api
def test_detokenize_fails(model: AlephAlphaModel):
    # given a client
    assert model.model_name in map(
        lambda model: model["name"], model.client.available_models()
    )

    # when posting an illegal request
    request = DetokenizationRequest([])

    # then we expect an exception tue to a bad request response from the API
    with pytest.raises(ValueError) as e:
        response = model.detokenize(request=request)

    assert e.value.args[0] == 400
