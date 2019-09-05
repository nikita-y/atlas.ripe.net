# #!/usr/bin/env python3

import json
import requests
import iterm2


async def main(connection):
    api_key = "atlas_api_key"
    knobs = [
        iterm2.StringKnob("API key", "API KEY", "", api_key)
    ]
    component = iterm2.StatusBarComponent(
        short_description="RIPE Atlas Credits",
        detailed_description="Shows credits balance at atlas.ripe.net",
        knobs=knobs,
        exemplar="0.0 / 34,000.0 / 4,000,000.0",
        update_cadence=300,
        identifier="com.iterm2.example.status-bar")

    @iterm2.StatusBarRPC
    async def coro(knobs):
        URL = 'https://atlas.ripe.net/api/v2/credits/'
        PARAMS = {'key': knobs[api_key]}
        try:
            r = requests.get(url=URL, params=PARAMS)
            data = r.json()
            daily = data['estimated_daily_income']
            total = data['current_balance']
            expenditure = data['estimated_daily_expenditure']
        except:
            raise
        else:
            return f'{float(expenditure):,.1f} / {float(daily):,.1f} / {float(total):,.1f}'

    await component.async_register(connection, coro)

iterm2.run_forever(main)
