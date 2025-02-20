from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from app import app

# Build the layout for the app. Using dash bootstrap container here instead of the standard html div.
# Container looks better
layout = dbc.Container([
    dbc.Tabs([
        dbc.Tab(label='Klima (4,4) Simulator',
                label_style={'background': 'linear-gradient(71.9deg, #00CC33 24.64%, #00771E 92.66%)'},
                tab_style={'background': 'linear-gradient(71.9deg, #00CC33 24.64%, #00771E 92.66%)',
                           'fontSize': '30px'},
                active_tab_style={'color': '#0ba1ff'},
                active_label_style={'color': '#222222'},
                children=[
                    dbc.Row([
                        dbc.Col(dbc.Card([
                            dbc.CardHeader('(4,4) Simulation parameters',
                                           className='enclosure_card_topic'),
                            dbc.CardBody([
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Label('Klima price (USDC)')
                                    ]),
                                    dbc.Col([
                                        dbc.Label('Starting amount of Klima (Units)')
                                    ]),
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Input(
                                            id='klima_price',
                                            placeholder='1000',
                                            type='number',
                                            min=1,
                                            step=0.001,
                                            debounce=True,
                                            value=800, className="input_box_number")]),
                                    dbc.Col([
                                        dbc.Input(
                                            id='initial_klima',
                                            placeholder='1',
                                            type='number',
                                            min=1,
                                            step=0.001,
                                            debounce=True,
                                            value=10, className="input_box_number")]),
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Label('Bond ROI (%)'),
                                    ]),
                                    dbc.Col([
                                        dbc.Label('Rebase Rate (%)'),
                                    ]),
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Input(
                                            id='bond_roi',
                                            placeholder='5',
                                            type='number',
                                            step=0.001,
                                            debounce=True,
                                            value=5,
                                            className="input_box_number"),
                                    ]),
                                    dbc.Col([
                                        dbc.Input(
                                            id='reward_yield',
                                            placeholder='0.5',
                                            type='number',
                                            step=0.001,
                                            debounce=True,
                                            value=0.5,
                                            className="input_box_number"),
                                    ])
                                ]),
                            ])
                        ], outline=True, color='success', style={"height": "100%"})),
                    ], style={'padding': '10px'}),
                    dbc.Row([
                        dbc.Col(dbc.Card([
                            dbc.CardHeader('(3,3) and (4,4) Growth comparison', className='enclosure_card_topic'),
                            dbc.CardBody([
                                dcc.Graph(id='graph2', style={"height": "100%", "width": "100%"}),
                            ], style={"height": "100%", "width": "100%"})
                        ], outline=False, color='#232b2b', style={"height": "100%", "width": "100%",
                                                                  'border-color': '#00cc33'}),
                            xs=12, sm=12, md=12, lg=8, xl=8),
                        dbc.Col(dbc.Card([
                            dbc.CardHeader('Growth Comparison Summary', className='enclosure_card_topic'),
                            dbc.CardBody([
                                    dbc.Row([
                                        dbc.Label('Max (3,3) ROI (Klima)', className='bonding_roi_card_topic'),
                                        html.Div(className="bonding_roi_card_metrics",
                                                 id='max_33_growth'),
                                        dcc.Markdown('---')
                                    ], className='text-center'),
                                    dbc.Row([
                                        dbc.Label('Max (4,4) ROI (Klima)', className="bonding_roi_card_topic"),
                                        html.Div(className="bonding_roi_card_metrics",
                                                 id='max_44_growth'),
                                        dcc.Markdown('---')
                                    ], className='text-center'),
                                    dbc.Row([
                                        dbc.Label('Bonus Klima', className="bonding_roi_card_topic"),
                                        html.Div(className="bonding_roi_card_metrics",
                                                 id='bonus_gained'),
                                    ], className='text-center')
                            ])
                        ], outline=True, color='success', style={"height": "100%", "width": "auto"}))
                    ], style={'padding': '10px'}),
                    dbc.Row([
                        dbc.Col(dbc.Card([
                            dbc.CardHeader('Chart Explanation', className='enclosure_card_topic'),
                            dbc.CardBody([
                                dcc.Markdown('''
                                This chart contains two trend lines (3,3) Klima Growth and (4,4) Klima Growth.
                                The (4,4) Klima growth trend line depicts the Klima growth based on claim/stake
                                frequency throughout the vesting period.
                                As we have learned in the Bonding: Learn page, bonding allows to purchase Klima at a
                                discount from the protocol.
                                Bonding provides an opportunity to acquire more Klimas when compared to market buying.
                                This opportunity could be further amplified by claiming/staking vested Klimas as
                                they become available to you.
                                Please see the ROI comparison chart for details on the effects of claiming/staking
                                frequency.
                                The (3,3) Klima growth trend line depicts Klima growth throughout the same vesting
                                period.
                                This chart compares simple staking (3,3) and the claim/stake (4,4) Klima growth
                                throughout the vesting period
                                (In KlimaDAO, the vesting period is 15 epochs, equivalent to 5 days).
                                ''')
                            ])
                        ], outline=True, color='success'), xs=12, sm=12, md=12, lg=12, xl=12)
                    ], className="mb-5"),
                    dbc.Row([
                        dbc.Col(
                            dbc.Card([
                                dbc.CardHeader('(3,3) and (4,4) ROI Comparison', className='enclosure_card_topic'),
                                dbc.CardBody([
                                    dcc.Graph(id='graph3', style={"height": "100%", "width": "100%"}),
                                ], style={"height": "100%", "width": "100%"})
                            ], outline=False, color='#232b2b', style={"height": "100%", "width": "100%",
                                                                      'border-color': '#00cc33'}),
                            xs=12, sm=12, md=12, lg=8, xl=8),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardHeader('(3,3) and (4,4) ROI Summary', className='enclosure_card_topic'),
                                dbc.CardBody([
                                    dbc.Row(
                                        dbc.Label('(3,3) ROI (%)', className='bonding_roi_card_topic'),
                                    ),
                                    dbc.Row(
                                        html.Div(className="bonding_roi_card_metrics",
                                                 id='33_roi'),
                                    ),
                                    dbc.Row(
                                        dbc.Row(
                                            dcc.Markdown('''
                                            ---
                                            ''')
                                        ),
                                    ),
                                    dbc.Row(
                                        dbc.Label('Bond ROI (%)', className="bonding_roi_card_topic"),
                                    ),
                                    dbc.Row(
                                        html.Div(className="bonding_roi_card_metrics",
                                                 id='bonding_roi'),
                                    ),
                                    dbc.Row(
                                        dbc.Row(
                                            dcc.Markdown('''
                                            ---
                                            ''')
                                        ),
                                    ),
                                    dbc.Row(
                                        dbc.Label('Max (4,4) ROI (%)', className="bonding_roi_card_topic"),
                                    ),
                                    dbc.Row(
                                        html.Div(className="bonding_roi_card_metrics",
                                                 id='max_44_roi'),
                                    ),
                                ])
                            ], outline=True, color='success', style={"height": "100%", "width": "auto"})],
                            xs=12, sm=12, md=12, lg=4, xl=4),
                    ], style={'padding': '10px'}),
                    dbc.Row([
                        dbc.Col(dbc.Card([
                            dbc.CardHeader('Chart Explanation', className='enclosure_card_topic'),
                            dbc.CardBody([
                                dcc.Markdown('''
                                This chart contains two trend lines (3,3) ROI and (4,4) ROI.
                                The (4,4) ROI trend line depicts the bonding ROI based on claim/stake frequency
                                throughout the vesting period.
                                For example, depending on the control parameters, the highest ROI could be achieved
                                by claiming/staking vested
                                Klima tokens before every epoch, halfway through, or maybe the first four epochs.
                                There might also be scenarios where it is not profitable for you to claim/stake
                                at all.
                                There could be many claim/stake combinations; the chart tries to predict the
                                best possible combination.
                                The (3,3) ROI trend line depicts plain staking ROI throughout the same vesting
                                period.
                                This chart compares simple staking (3,3) and the claim/stake (4,4) ROIs throughout
                                the vesting period
                                (In KlimaDAO, the vesting period is 15 epochs, equivalent to 5 days).
                                ''')
                            ])
                        ], outline=True, color='success'), xs=12, sm=12, md=12, lg=12, xl=12)
                    ], className="mb-5"),
                    ]),
        dbc.Tab(label='Guide',
                label_style={'background': 'linear-gradient(71.9deg, #00CC33 24.64%, #00771E 92.66%)',
                             'fontSize': '30px'},
                tab_style={'background': 'linear-gradient(71.9deg, #00CC33 24.64%, #00771E 92.66%)'},
                active_tab_style={'background': '#0ba1ff', 'fontSize': '30px'},
                active_label_style={'color': '#222222'},
                children=[
                    dbc.Row([
                        html.Div(html.Img(src=app.get_asset_url('PG_Bonding_Learn.png'),
                                          style={'height': '100%',
                                                 'width': '100%',
                                                 'padding': '10px'}))])
                ])
    ], className='mb-4'),
], fluid=True)  # Responsive ui control


@app.callback([
    Output(component_id='graph2', component_property='figure'),
    Output(component_id='graph3', component_property='figure'),
    Output(component_id='max_33_growth', component_property='children'),
    Output(component_id='max_44_growth', component_property='children'),
    Output(component_id='bonus_gained', component_property='children'),
    Output(component_id='33_roi', component_property='children'),
    Output(component_id='bonding_roi', component_property='children'),
    Output(component_id='max_44_roi', component_property='children'),
    Input(component_id='klima_price', component_property='value'),
    Input(component_id='initial_klima', component_property='value'),
    Input(component_id='bond_roi', component_property='value'),
    Input(component_id='reward_yield', component_property='value'),
])
# region Description: Function to calculate Klima growth over time
def bonding_simulation(klima_price, initial_klima, bond_roi, reward_yield):
    # Protocol and Klima calcs:
    usd_bonded = klima_price * initial_klima
    bond_roi = (bond_roi / 100)
    bond_price = klima_price / (1 + bond_roi)
    bonded_klima = usd_bonded / bond_price
    bonded_klimaValue = bonded_klima * klima_price
    gwei = 0
    priceofETH = 1
    # ========================================================================================
    # Calculate the rebase rate and Current APY (next epoch rebase pulled from hippo data source)
    reward_yield = reward_yield / 100
    # rebase_const = 1 + reward_yield  # calculate a constant for use in APY calculation
    # user_apy = rebase_const ** 1095  # current APY equation
    # user_apy_P = user_apy * 100  # convert to %
    # ========================================================================================
    # Calculate fees
    staking_gas_fee = 179123 * ((gwei * priceofETH) / (10 ** 9))
    unstaking_gas_fee = 89654 * ((gwei * priceofETH) / (10 ** 9))
    swapping_gas_fee = 225748 * ((gwei * priceofETH) / (10 ** 9)) + ((0.3 / 100) * bonded_klimaValue)
    claim_gas_fee = 80209 * ((gwei * priceofETH) / (10 ** 9))
    bonding_gas_fee = 258057 * ((gwei * priceofETH) / (10 ** 9))
    # ================================================================================

    claim_stake_gas_fee = staking_gas_fee + claim_gas_fee
    remaining_gas_fee = bonding_gas_fee + unstaking_gas_fee + swapping_gas_fee
    # ================================================================================
    # (3,3) Rate for the 15 epochs
    staking_reward_rate = (1 + reward_yield) ** 15 - 1
    staking_reward_rate_P = round(staking_reward_rate * 100, 2)
    # ================================================================================
    vested_klima_df = pd.DataFrame(np.arange(1, 16), columns=['Epochs'])
    vested_klima_df['Days'] = vested_klima_df.Epochs / 3
    vested_klima_growth = np.array([], dtype=np.float64)
    bond_roi_growth = np.array([], dtype=np.float64)

    staked_klima_roi_df = pd.DataFrame(np.arange(1, 16), columns=['Epochs'])
    staked_klima_roi_df['Days'] = staked_klima_roi_df.Epochs / 3
    staked_roi_adjusted_growth = np.array([], dtype=np.float64)
    stake_roi_growth = np.array([], dtype=np.float64)
    staked_klima_growth = np.array([], dtype=np.float64)
    stake_growth = initial_klima

    for epochs in vested_klima_df.Epochs:
        vested_klima = ((bonded_klima / (1 + epochs)) * (((1 + reward_yield) ** 15) - 1)) \
                       / ((1 + reward_yield) ** (15 / (1 + epochs)) - 1)
        vested_klima_roi = (((vested_klima * klima_price - epochs * claim_stake_gas_fee
                              - remaining_gas_fee) / usd_bonded) - 1) * 100
        vested_klima_growth = np.append(vested_klima_growth, vested_klima)
        bond_roi_growth = np.append(bond_roi_growth, vested_klima_roi)
    vested_klima_df['vested_klimas'] = vested_klima_growth
    vested_klima_df['Bond_ROI'] = bond_roi_growth

    for epochs in staked_klima_roi_df.Epochs:
        staked_klima_growth = np.append(staked_klima_growth, stake_growth)
        staked_roi_adjusted = ((usd_bonded - staking_gas_fee) * (((1 + reward_yield) ** 15) / usd_bonded) - 1) * 100
        stake_roi = staking_reward_rate * 100
        stake_growth = stake_growth * (1 + reward_yield)
        staked_roi_adjusted_growth = np.append(staked_roi_adjusted_growth, staked_roi_adjusted)
        stake_roi_growth = np.append(stake_roi_growth, stake_roi)
    staked_klima_roi_df['Stake_ROI'] = stake_roi_growth
    staked_klima_roi_df['Staked_feeAdjustedROI'] = staked_roi_adjusted_growth
    staked_klima_roi_df['Stake_Growth'] = staked_klima_growth
    # ================================================================================

    cols_to_use = staked_klima_roi_df.columns.difference(vested_klima_df.columns)
    stake_bond_df = pd.merge(vested_klima_df, staked_klima_roi_df[cols_to_use],
                             left_index=True, right_index=True, how='outer')

    maxbond_roi = round(stake_bond_df.Bond_ROI.max(), 2)
    maxstake_growth = round(stake_bond_df.Stake_Growth.max(), 2)
    maxBondGrowth = round(stake_bond_df.vested_klimas.max(), 2)
    klimaGained = round((stake_bond_df.vested_klimas.max() - stake_bond_df.Stake_Growth.max()), 2)
    bond_roi_percent = bond_roi * 100

    stake_bond_chart = go.Figure()
    stake_bond_chart.add_trace(go.Scatter(x=stake_bond_df.Epochs, y=stake_bond_df.vested_klimas,
                                          name='(4,4) Growth', fill=None, line=dict(color='#00aff3', width=2)))
    stake_bond_chart.add_trace(go.Scatter(x=stake_bond_df.Epochs, y=stake_bond_df.Stake_Growth,
                                          name='(3,3) Growth', line=dict(color='#ff2a0a', width=2)))

    stake_bond_chart.update_layout(autosize=True, showlegend=True, margin=dict(l=20, r=30, t=10, b=20))
    stake_bond_chart.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
                                   xaxis_title="Epochs (Vesting period)", yaxis_title="Total Klimas")
    stake_bond_chart.update_layout({'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0, 0, 0, 0)'})

    stake_bond_chart.update_xaxes(showline=True, linewidth=0.1, linecolor='#31333F', color='white',
                                  showgrid=False, gridwidth=0.1, mirror=True)
    stake_bond_chart.update_yaxes(showline=True, linewidth=0.1, linecolor='#31333F', color='white',
                                  showgrid=False, gridwidth=0.01, mirror=True)
    stake_bond_chart.layout.legend.font.color = 'white'

    # =============================

    stake_bond_roi_chart = go.Figure()

    stake_bond_roi_chart.add_trace(go.Scatter(x=stake_bond_df.Epochs, y=stake_bond_df.Bond_ROI, name='(4,4) ROI ',
                                              line=dict(color='#00aff3', width=2)))
    stake_bond_roi_chart.add_trace(go.Scatter(x=stake_bond_df.Epochs, y=stake_bond_df.Stake_ROI, name='(3,3) ROI ',
                                              fill=None, line=dict(color='#ff2a0a', width=2)))

    stake_bond_roi_chart.update_layout(autosize=True, showlegend=True, margin=dict(l=20, r=30, t=10, b=20))
    stake_bond_roi_chart.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
                                       xaxis_title="Epochs (Vesting period)",
                                       yaxis_title="ROI based on claim/stake frequency")
    stake_bond_roi_chart.update_layout({'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0, 0, 0, 0)'})

    stake_bond_roi_chart.update_xaxes(showline=True, linewidth=0.1, linecolor='#31333F', color='white',
                                      showgrid=False, gridwidth=0.1, mirror=True)
    stake_bond_roi_chart.update_yaxes(showline=True, linewidth=0.1, linecolor='#31333F', color='white',
                                      showgrid=False, gridwidth=0.01, mirror=True)
    stake_bond_roi_chart.layout.legend.font.color = 'white'

    return stake_bond_chart, stake_bond_roi_chart, maxstake_growth, maxBondGrowth, \
        klimaGained, staking_reward_rate_P, \
        bond_roi_percent, maxbond_roi  # noqa: E127
