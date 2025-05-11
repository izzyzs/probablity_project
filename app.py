import streamlit as st

# import pandas as pd
import math as m

st.title("Project 3: Deal Site Visualizer")

with st.sidebar:
    st.subheader("Initial Values")
    with st.container(border=True):
        st.latex(r"""\theta""")
        theta = st.slider("The probability of the merchant being an H-type", 0.01, 1.0)
        st.text("NOTE: you must select alpha_L before alpha_H")
        st.latex(r"""\alpha_L""")
        alpha_l = st.slider("The probability of fit for type L merchant", 0.01, 1.0)
        st.latex(r"""\alpha_H""")
        alpha_h = st.slider(
            "The probability of fit for type H merchant", alpha_l + 0.01, 1.0
        )
        st.latex(r"""N""")
        n = st.slider("Number of new consumers on the website", 1)
        st.latex(r"""\beta""")
        beta = st.slider("Proportion of infrequent visitors on the site", 0.01, 1.0)
        st.latex(r"""p""")
        p = st.slider("Merchant's regular price", 0.01, 1.0)


def get_equilibrium(e):
    match e:
        case 1:
            return "Distortionless Separating Equilibrium"
        case 2:
            return "Pooling Equilibrium"
        case 3:
            return "Separating Equilibrium with Price Distortion"
        case 0:
            return "Not Found"


st.subheader("Which Equilibrium?")
with st.container(border=True):
    st.markdown("##### Is it a Distortionless Separating Equilibrium?")
    st.text("Distortionless Separating Equilibrium condition:")
    st.latex(
        r"""\alpha_L \in [\alpha_2, \alpha_H)\ where\ \alpha_2 = \frac{1}{2}[\sqrt{N^2 - 2N(1-\beta)\alpha_H + \alpha^2_H} - (N - \alpha_H)]"""
    )
    alpha_2 = (1 / 2) * (
        (((n**2) - (2 * n * (1 - beta) * alpha_h) + (alpha_h**2)) ** 0.5)
        - (n - alpha_h)
    )
    st.latex(
        "\\alpha_L = "
        + str(alpha_l)
        + " \\in ["
        + str(alpha_2)
        + ", "
        + str(alpha_h)
        + ")"
    )
    st.latex(r"""\alpha_2 = """ + str(alpha_2))

    st.markdown("#####  is it a pooling equilibrium?")
    st.text("Pooling Equilibrium condition:")
    st.latex(r"""\alpha_L \in (0, \alpha_2)\ where""")
    st.latex(
        r"""\alpha_2 = \frac{1}{2}[\sqrt{N^2 - 2N(1-\beta)\alpha_H + \alpha^2_H} - (N - \alpha_H)]"""
    )
    st.latex("\\alpha_L = " + str(alpha_l) + " \\in [0, " + str(alpha_2) + ")")
    st.latex(r"""and""")
    st.latex(r""" \theta \in (max\{\theta_1, \theta_2\}, 1)""")
    theta_1 = ((p * alpha_h) - (alpha_l * (n + alpha_h))) / (
        (n + alpha_h) * (alpha_h - alpha_l)
    )
    theta_2 = (n * alpha_l * (1 - ((1 / 2) * beta))) / (
        (alpha_l + ((1 / 2) * beta * n) * (alpha_h - alpha_l))
    )
    st.latex(r"""\theta_1 = """ + str(theta_1))
    st.latex(r"""\theta_2 = """ + str(theta_2))
    st.latex(
        "\\theta = "
        + str(theta)
        + " \\in (max\\{"
        + str(theta_1)
        + ", "
        + str(theta_2)
        + "\\}, 1)"
    )

    st.markdown("##### is it a separating equilibrium with price distortion?")
    st.text("Separating Equilibrium with Price Distortion conditions:")
    st.latex("\\alpha_L \\in (\\alpha_3, \\alpha_2)")
    st.latex(
        "where\\ \\alpha_3 = \\frac{\\sqrt{(N^2 + (N-p)\\alpha_H)^2 + 2p\\beta N\\alpha_H(N+\\alpha_H)}+p\\alpha_H-N(N+\\alpha_H)}{2(N+\\alpha_H)}"
    )
    st.latex("\\theta \\in (0, \\theta_2]")
    term_1 = (n**2 + ((n - p) * alpha_h)) ** 2
    term_2 = 2 * p * beta * n * alpha_h * (n + alpha_h)
    numerator = m.sqrt(term_1 + term_2) + (p * alpha_h) - (n * (n + alpha_h))
    denominator = 2 * (n + alpha_h)
    alpha_3 = numerator / denominator

    st.latex(r"""\alpha_3 = """ + str(alpha_3))
    st.latex(
        "\\alpha_L = "
        + str(alpha_l)
        + " \\in ("
        + str(alpha_3)
        + ", "
        + str(alpha_2)
        + ")"
    )

    distortionless_separating = alpha_l >= alpha_2 and alpha_l < alpha_h

    alpha_l_condition_pool = alpha_l > 0 and alpha_l < alpha_2
    theta_condition_pool = theta > max(theta_1, theta_2) and theta < 1
    pooling = alpha_l_condition_pool and theta_condition_pool

    alpha_l_condition_dist = alpha_l > alpha_3 and alpha_l < alpha_2
    theta_condition_dist = theta > 0 and theta <= theta_2
    distortion = alpha_l_condition_dist and theta_condition_dist

    equilibrium = (
        1 if distortionless_separating else (2 if pooling else (3 if distortion else 0))
    )
    st.title("Equilibrium: " + get_equilibrium(equilibrium))


def find_prices_and_revenue(e):
    l_type_deal_price = 0
    h_type_deal_price = 0
    l_type_deal_revenue = 0
    h_type_deal_revenue = 0
    consumer_decision_process = ""
    match e:
        case 1:
            l_type_deal_price = alpha_l
            l_type_deal_revenue = alpha_l * (alpha_l + n)
            h_type_deal_price = alpha_h
            h_type_deal_revenue = alpha_h * (alpha_h + n)
            consumer_decision_process = r"""
                Early-new: purchase based on price
                Frequent-new and late-new: wait till period 2 and purchase based on sales
                Experienced: purchase based on matching
            """
        case 2:
            alpha_with_macron = (theta * alpha_h) + ((1 - theta) * alpha_l)
            l_type_deal_price = alpha_with_macron
            l_type_deal_revenue = alpha_with_macron * (alpha_l + (0.5 * beta * n))
            h_type_deal_price = alpha_with_macron
            h_type_deal_revenue = alpha_with_macron * (alpha_h + n)
            consumer_decision_process = r"""
                Early-new: purchase based on assumption (as there exists no means of verifying type)
                Frequent-new and late-new: wait till period 2 and purchase based on sales
                Experienced: purchase based on matching
            """
        case 3:
            d_star_h = (alpha_l * (alpha_l + n)) / (alpha_l + (0.5 * beta * n))
            l_type_deal_price = alpha_l
            l_type_deal_revenue = alpha_l * (alpha_l + n)
            h_type_deal_price = d_star_h
            h_type_deal_revenue = d_star_h * (alpha_h + n)
            consumer_decision_process = r"""
                Early-new: purchase based on price.
                Frequent-new and late-new: wait till period 2 and purchase based on sales.
                Experienced: purchase based on matching.

            note: The consumer's decision making in this equilibrium is equal to their decision making in a Distortionles Separating Equilibrium.
            """

    return {
        "l_type_deal_price": l_type_deal_price,
        "l_type_deal_revenue": l_type_deal_revenue,
        "h_type_deal_price": h_type_deal_price,
        "h_type_deal_revenue": h_type_deal_revenue,
        "consumer_decision_process": consumer_decision_process,
    }


st.subheader(f"Revenue Projections for this {get_equilibrium(equilibrium)}")
with st.container(border=True):
    output = find_prices_and_revenue(equilibrium)
    st.text(f"L-type deal price: {output["l_type_deal_price"]}")
    st.text(f"L-type deal revenue: {output["l_type_deal_revenue"]}")
    st.text(f"H-type deal price: {output["h_type_deal_price"]}")
    st.text(f"H-type deal revenue: {output["h_type_deal_revenue"]}")
    st.text(f"Consumer decision making process: {output["consumer_decision_process"]}")
