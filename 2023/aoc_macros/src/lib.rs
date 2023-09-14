extern crate proc_macro;
use proc_macro::{TokenStream};

use quote::quote;
use syn::{parse_macro_input, DeriveInput, Attribute, DataStruct};

#[proc_macro_derive(AoCSetup)]
pub fn aoc_day(item: TokenStream) -> TokenStream {
    let ast = syn::parse_macro_input!(item as syn::ItemStruct);

    let ident = &ast.ident;
    let fpath = format!("input/{}.txt", ast.ident.to_string().to_lowercase());

    quote! {
        use crate::{AoCSetup};
        impl AoCSetup for #ident {
            fn new() -> Box<Self> {
                Box::new(#ident::default())
            }
        
            #[inline]
            fn input(&self) -> &'static str {
                include_str!(#fpath)
            }
        }
        
    }.into()
}