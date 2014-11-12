import pymel.core as pc

def _add():
    objects = pc.ls(sl=True)
    if not objects:
        pc.warning('No objects selected...')
        return
    shadingEngines = set()
    for obj in objects:
        for engine in pc.listConnections(obj, type='shadingEngine'):
            shadingEngines.add(engine)
    if not shadingEngines:
        pc.warning("No shading engine found...")
    aicmd = 'createRenderNodeCB -asShader "surfaceShader" aiShadowCatcher ""'
    try:
        arnold = pc.PyNode(pc.Mel.eval(aicmd))
    except:
        pc.warning("Seems like Arnod is either not installed or not loaded")
        return
    for engin in pc.listConnections(arnold, type='shadingEngine'):
        pc.delete(engin)
    errors = []
    for eng in shadingEngines:
        try:
            pc.editRenderLayerAdjustment(eng.surfaceShader)
            arnold.outColor.connect(eng.surfaceShader, f=True)
        except:
            errors.append(eng)
    pc.warning('Following engines could not connect')
    for error in errors:
        print error