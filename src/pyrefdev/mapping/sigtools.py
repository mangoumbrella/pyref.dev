VERSION = "4.0.1"

# fmt: off
MAPPING = {
    "sigtools": "https://sigtools.readthedocs.io/en/stable/",
    "sigtools.modifiers": "https://sigtools.readthedocs.io/en/stable/api.html#module-sigtools.modifiers",
    "sigtools.modifiers.annotate": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.modifiers.annotate",
    "sigtools.modifiers.autokwoargs": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.modifiers.autokwoargs",
    "sigtools.modifiers.kwoargs": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.modifiers.kwoargs",
    "sigtools.modifiers.posoargs": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.modifiers.posoargs",
    "sigtools.signature": "https://sigtools.readthedocs.io/en/stable/signature-retrieval.html#sigtools.signature",
    "sigtools.signatures": "https://sigtools.readthedocs.io/en/stable/api.html#module-sigtools.signatures",
    "sigtools.signatures.apply_params": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.signatures.apply_params",
    "sigtools.signatures.embed": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.signatures.embed",
    "sigtools.signatures.forwards": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.signatures.forwards",
    "sigtools.signatures.incompatiblesignatures": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.signatures.IncompatibleSignatures",
    "sigtools.signatures.mask": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.signatures.mask",
    "sigtools.signatures.merge": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.signatures.merge",
    "sigtools.signatures.signature": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.signatures.signature",
    "sigtools.signatures.sort_params": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.signatures.sort_params",
    "sigtools.signatures.upgradedannotation": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.signatures.UpgradedAnnotation",
    "sigtools.signatures.upgradedannotation.preevaluated": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.signatures.UpgradedAnnotation.preevaluated",
    "sigtools.signatures.upgradedannotation.source_value": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.signatures.UpgradedAnnotation.source_value",
    "sigtools.signatures.upgradedannotation.upgrade": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.signatures.UpgradedAnnotation.upgrade",
    "sigtools.signatures.upgradedparameter": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.signatures.UpgradedParameter",
    "sigtools.signatures.upgradedparameter.evaluated": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.signatures.UpgradedParameter.evaluated",
    "sigtools.signatures.upgradedparameter.replace": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.signatures.UpgradedParameter.replace",
    "sigtools.signatures.upgradedparameter.source_depths": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.signatures.UpgradedParameter.source_depths",
    "sigtools.signatures.upgradedparameter.sources": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.signatures.UpgradedParameter.sources",
    "sigtools.signatures.upgradedparameter.upgraded_annotation": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.signatures.UpgradedParameter.upgraded_annotation",
    "sigtools.signatures.upgradedsignature": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.signatures.UpgradedSignature",
    "sigtools.signatures.upgradedsignature.evaluated": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.signatures.UpgradedSignature.evaluated",
    "sigtools.signatures.upgradedsignature.parameters": "https://sigtools.readthedocs.io/en/stable/signature-retrieval.html#sigtools.signatures.UpgradedSignature.parameters",
    "sigtools.signatures.upgradedsignature.replace": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.signatures.UpgradedSignature.replace",
    "sigtools.signatures.upgradedsignature.sources": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.signatures.UpgradedSignature.sources",
    "sigtools.signatures.upgradedsignature.upgraded_return_annotation": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.signatures.UpgradedSignature.upgraded_return_annotation",
    "sigtools.specifiers": "https://sigtools.readthedocs.io/en/stable/api.html#module-sigtools.specifiers",
    "sigtools.specifiers.apply_forwards_to_super": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.specifiers.apply_forwards_to_super",
    "sigtools.specifiers.as_forged": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.specifiers.as_forged",
    "sigtools.specifiers.forger_function": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.specifiers.forger_function",
    "sigtools.specifiers.forwards": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.specifiers.forwards",
    "sigtools.specifiers.forwards_to_function": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.specifiers.forwards_to_function",
    "sigtools.specifiers.forwards_to_method": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.specifiers.forwards_to_method",
    "sigtools.specifiers.forwards_to_super": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.specifiers.forwards_to_super",
    "sigtools.specifiers.set_signature_forger": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.specifiers.set_signature_forger",
    "sigtools.specifiers.signature": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.specifiers.signature",
    "sigtools.sphinxext": "https://sigtools.readthedocs.io/en/stable/api.html#module-sigtools.sphinxext",
    "sigtools.support": "https://sigtools.readthedocs.io/en/stable/api.html#module-sigtools.support",
    "sigtools.support.assert_func_sig_coherent": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.support.assert_func_sig_coherent",
    "sigtools.support.bind_callsig": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.support.bind_callsig",
    "sigtools.support.f": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.support.f",
    "sigtools.support.func_code": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.support.func_code",
    "sigtools.support.func_from_sig": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.support.func_from_sig",
    "sigtools.support.make_func": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.support.make_func",
    "sigtools.support.make_up_callsigs": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.support.make_up_callsigs",
    "sigtools.support.read_sig": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.support.read_sig",
    "sigtools.support.s": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.support.s",
    "sigtools.support.sort_callsigs": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.support.sort_callsigs",
    "sigtools.wrappers": "https://sigtools.readthedocs.io/en/stable/api.html#module-sigtools.wrappers",
    "sigtools.wrappers.combination": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.wrappers.Combination",
    "sigtools.wrappers.combination.get_signature": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.wrappers.Combination.get_signature",
    "sigtools.wrappers.decorator": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.wrappers.decorator",
    "sigtools.wrappers.wrapper_decorator": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.wrappers.wrapper_decorator",
    "sigtools.wrappers.wrappers": "https://sigtools.readthedocs.io/en/stable/api.html#sigtools.wrappers.wrappers",
}
