module FinancialBVAR

using Distributions

    using LinearAlgebra

    export NormalWishartBVARmodel, NormalWishartBVAR, sample_posterior!

    mutable struct NormalWishartBVARmodel
        const Y:: AbstractArray
        const X:: AbstractArray
        const C_OLS:: AbstractArray
        const S_OLS:: AbstractArray
        const df:: Int64
        Σ:: Union{AbstractArray,Missing} 
        Β:: Union{AbstractArray,Missing} 
    end

    function NormalWishartBVAR(data)
        p = 1   #lag
        T,n  = size(data)
        df = T -1 - n
        Y = data[p+1:end,:]
        X = hcat(ones(T-1), data[p:end-1,:])
        C = inv(transpose(X) * X) * transpose(X) * Y
        S = transpose((Y - X*C)) * (Y - X*C)
       
        return NormalWishartBVARmodel(Y, X, C, S, df, missing, missing)
    end

    function sample_posterior!(model :: NormalWishartBVARmodel)
        Sigma = rand(InverseWishart(model.df,model.S_OLS),5)
        model.Σ = Sigma

        Beta_mean = vec(model.C_OLS)
        Beta_var = kron(model.Σ[1],inv(transpose(model.X) * model.X))
        Beta = rand(MvNormal(Beta_mean,Beta_var),5)
        model.Β = Beta
    end

end